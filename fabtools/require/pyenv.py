from fabric.api import hide, run, settings
from fabtools import require
from fabtools.pyenv import install


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
