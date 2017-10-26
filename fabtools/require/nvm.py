from fabric.api import hide, run, settings
from fabtools import require, files
from fabtools.nvm import (
    install, install_node, NODE_DEPENDENCIES
)


def nvm():
    """
    Require installed nvm
    """
    if not files.exists("~/.nvm"):
        require.curl.command()
        install()


def node(version):
    """
    Require specific node version to be installed

    :param version: node version
    """
    require.deb.packages(NODE_DEPENDENCIES)
    install_node(version)
