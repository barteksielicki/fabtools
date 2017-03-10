import os

from fabric.api import cd, run, sudo
from fabtools import files

UWSGI_DOWNLOAD_URL = "https://projects.unbit.it/downloads/uwsgi-latest.tar.gz"

UWSGI_BINARY_PATH = "/usr/local/bin/uwsgi"

UWSGI_INSTALLATION_DIR = "/opt/uwsgi"

UWSGI_PLUGINS_LOCATION = "/etc/uwsgi/plugins"

UWSGI_SITES_LOCATION = "/etc/uwsgi/sites"

UWSGI_SERVICE_TEMPLATE = """\
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --emperor {emperor_dir} --die-on-term
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGTERM
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
""".format(emperor_dir=UWSGI_SITES_LOCATION)


def is_installed():
    return files.exists(UWSGI_BINARY_PATH)


def plugin_exists(name):
    return files.exists(os.path.join(
        UWSGI_PLUGINS_LOCATION, "{0}_plugin.so".format(name))
    )


def manual_install():
    """
    Perform installation of uwsgi from source,
    so python plugins could be installed
    """
    if not is_installed():
        tmp_archive = "uwsgi.tar.gz"

        with cd("/tmp"):
            run("wget {0} -O {1}".format(UWSGI_DOWNLOAD_URL, tmp_archive))
            run("tar xzf {0}".format(tmp_archive))
            files.remove(tmp_archive)
            if files.is_dir(UWSGI_INSTALLATION_DIR):
                files.remove(UWSGI_INSTALLATION_DIR, True, use_sudo=True)
            sudo("mv uwsgi* {0}".format(UWSGI_INSTALLATION_DIR))
            with cd(UWSGI_INSTALLATION_DIR):
                run("make PROFILE=nolang")
                files.symlink(
                    os.path.join(UWSGI_INSTALLATION_DIR, "uwsgi"),
                    UWSGI_BINARY_PATH, use_sudo=True
                )
