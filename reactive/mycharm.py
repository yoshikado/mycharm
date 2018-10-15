from charmhelpers.core import hookenv, host
import charmhelpers.fetch as fetch
from charms.reactive import (
    set_state,
)
from charms.reactive.decorators import (
    hook,
    when,
    when_not,
)
import mycharm_implementation


@when_not('mycharm.installed')
def install():
    pkgs = mycharm_implementation.packages_to_install()
    hookenv.status_set('maintenance', 'Installing ' + ', '.join(pkgs))
    fetch.apt_install(pkgs, fatal=True)
    hookenv.status_set('maintenance', 'Installed required packages')
    set_state('mycharm.installed')


@when('mycharm.installed')
@when('config.changed')
def write_config():
    mycharm_ip = hookenv.config('mycharm-ip')
    mycharm_username = hookenv.config('mycharm-username')
    mycharm_password = hookenv.config('mycharm-password')
    mycharm_implementation.set_config({
        'mycharm_ip': mycharm_ip,
        'mycharm_username': mycharm_username,
        'mycharm_password': mycharm_password,
    })
    assess_status()


@hook('update-status')
def assess_status():
    package = mycharm_implementation.package_name()
    version = fetch.get_upstream_version(package)
    if version is not None:
        hookenv.application_version_set(version)

    # service status
    if host.service_running(mycharm_implementation.service_name()):
        hookenv.status_set('active', 'Ready')
    else:
        hookenv.status_set('blocked', 'Not running')
