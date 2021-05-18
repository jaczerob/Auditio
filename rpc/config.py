import configparser

_CONFIG_FILE = 'config.ini'
_CONFIG = configparser.ConfigParser()
_CONFIG.read(_CONFIG_FILE)


def get(section, option, fallback=None) -> str:
    return _CONFIG.get(section, option, fallback=fallback)


def write(section, option, value):
    _CONFIG.set(section, option, value)
    _CONFIG.write(open(_CONFIG_FILE))
