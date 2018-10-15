import charmhelpers.contrib.templating.jinja as templating


def config_file():
    return "/etc/mycharm.conf"


def _config_file_template():
    return "mycharm.conf"


def packages_to_install():
    return [package_name()]


def package_name():
    return "apache2"


def service_name():
    return "apache2"


def set_config(config):
    with open(config_file(), "w") as conffile:
        conffile.write(templating.render(_config_file_template(), config))
