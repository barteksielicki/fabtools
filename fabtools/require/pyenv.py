from fabric.api import hide, run, settings
from fabtools import require
from fabtools.pyenv import (
    install, python_version_installed, install_python, venv_exists,
    PYTHON_DEPENDENCIES, create_venv
)


def pyenv():
    """
    Require installed pyenv
    """
    with settings(
            hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        pyenv_root = run("which pyenv")
    if not pyenv_root:
        require.curl.command()
        install()


def python(version):
    """
    Require specific python version to be installed

    :param version: python version
    """
    if not python_version_installed(version):
        require.deb.packages(PYTHON_DEPENDENCIES)
        install_python(version)


def venv(name, version):
    """
    Require pyenv virtualenv to be installed

    :param name: virtualenv name
    :param version: python version
    """
    if not venv_exists(name):
        create_venv(name, version)
