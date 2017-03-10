from fabric.api import cd, env, sudo
from fabtools import require, files
from fabtools import uwsgi as _uwsgi
from fabtools.require.files import template_file
from fabtools.system import distrib_family, UnsupportedFamily


def uwsgi(as_service=True):
    """
    Require installed uwsgi package
    :param as_service: if True, uwsgi will be configured as systemd service
    """
    family = distrib_family()
    if family == 'debian':
        _uwsgi_debian(as_service)
    else:
        raise UnsupportedFamily(supported=['debian'])


def _uwsgi_debian(as_service=True, use_pip=False):
    """
    Require installed uwsgi package on debian family systems
    :param as_service: if True, uwsgi will be configured as systemd service
    """
    require.deb.package("python-dev")  # required to compile uwsgi
    if use_pip:
        require.python.package("uwsgi")
    else:
        _uwsgi.manual_install()
    if as_service:
        require.file(
            "/etc/systemd/system/uwsgi.service",
            _uwsgi.UWSGI_SERVICE_TEMPLATE.format(
                owner=env.user, group="www-data"
            ), use_sudo=True)
        require.directory("/etc/uwsgi/sites", use_sudo=True)
        require.service.started("uwsgi")


def python_plugin(path, name):
    """
    Require python plugin to be built and present
    :param path: absolute path to python executable
    :param name: name for new plugin
    """
    require.directory(_uwsgi.UWSGI_PLUGINS_LOCATION, use_sudo=True)
    if not _uwsgi.plugin_exists(name):
        with cd(_uwsgi.UWSGI_INSTALLATION_DIR):
            cmd = "PYTHON={path} ./uwsgi --build-plugin \"plugins/python {name}\""
            sudo(cmd.format(**locals()))
            files.move(
                "{0}_plugin.so".format(name), _uwsgi.UWSGI_PLUGINS_LOCATION,
                use_sudo=True
            )


def site(site_name, context, template_contents=None, template_source=None):
    config_filename = "/etc/uwsgi/sites/{0}.ini".format(site_name)
    template_file(config_filename, template_contents, template_source,
                  context, use_sudo=True)
