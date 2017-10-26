import os
from contextlib import contextmanager

from fabric.api import run, settings, hide, prefix
from fabric.contrib.files import append

NODE_DEPENDENCIES = [
    "make", "build-essential", "libssl-dev", "zlib1g-dev", "libbz2-dev",
    "libreadline-dev", "llvm", "libncurses5-dev",
    "libncursesw5-dev", "xz-utils"
]


def install():
    # use nvm-installer
    run("curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.6/install.sh | bash")
    append("~/.bash_profile", [
        'export NVM_DIR="$HOME/.nvm"',
        '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm',
        '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion'
    ])

def install_node(version):
    """
    Install given node version
    :param version: version of node
    """
    run("nvm install {0}".format(version))


@contextmanager
def use_version(version):
    """
    Context manager to use given node version
    :param name: node version to use
    """
    activate_venv_command = "nvm use {0}".format(name)
    with prefix(activate_venv_command):
        yield
