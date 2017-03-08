import os

from fabric.api import run
from fabric.contrib.files import append

def install():
    # use pyenv-installer
    run("curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash")
    pyenv_root = os.path.join(run("echo $HOME"), ".pyenv")
    append("~/.bash_profile", [
        'export PATH="{0}/bin:$PATH"'.format(pyenv_root),
        'eval "$(pyenv init -)"',
        'eval "$(pyenv virtualenv-init -)"'
    ])