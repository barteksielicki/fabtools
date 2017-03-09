import os
from contextlib import contextmanager

from fabric.api import run, settings, hide, prefix
from fabric.contrib.files import append

PYTHON_DEPENDENCIES = [
    "make", "build-essential", "libssl-dev", "zlib1g-dev", "libbz2-dev",
    "libreadline-dev", "libsqlite3-dev", "llvm", "libncurses5-dev",
    "libncursesw5-dev", "xz-utils"
]


def install():
    # use pyenv-installer
    run(
        "curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash")
    pyenv_root = os.path.join(run("echo $HOME"), ".pyenv")
    append("~/.bash_profile", [
        'export PATH="{0}/bin:$PATH"'.format(pyenv_root),
        'eval "$(pyenv init -)"',
        'eval "$(pyenv virtualenv-init -)"'
    ])


def python_version_installed(version):
    """
    Check if given version of python is alrady installed and present

    :param version: version of python
    :return: bool
    """
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        versions = run("pyenv versions --bare").split()
        return version in versions


def install_python(version):
    """
    Install given python version
    :param version: version of python
    """
    run("pyenv install {0}".format(version))


def venv_exists(name):
    """
    Check if virtualenv with given name exists

    :param name: virtualenv name
    :return:
    """
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        venvs = run("pyenv versions --bare").split()
        return name in venvs


def create_venv(name, version, force=True):
    """
    Create new virtualenv

    :param name: name
    :param version: version
    :param force: if venv with such name but different version already exists
    overwrite version.
    """
    opts = "-f" if force else ""
    run("pyenv virtualenv {opts} {version} {name}".format(**locals()))


@contextmanager
def venv(name):
    """
    Context manager to activate given virtualenv
    :param name: virtualenv name
    """
    activate_venv_command = "pyenv activate {0}".format(name)
    with prefix(activate_venv_command):
        yield
