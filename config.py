import configparser


_CONFIG = configparser.ConfigParser()
_CONFIG.read('./Resources/config.ini')


def get(section, option, fallback=None):
    return _CONFIG.get(section, option, fallback=fallback)


def write(section, option, value):
    _CONFIG.set(section, option, value)
