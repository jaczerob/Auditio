import logging

_FORMATTER = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
_LOGGER = logging.getLogger()

_LOGGER.setLevel(logging.DEBUG)

_FILE_HANDLER = logging.FileHandler('amrpc.log')
_FILE_HANDLER.setFormatter(_FORMATTER)
_LOGGER.addHandler(_FILE_HANDLER)

_CONSOLE_HANDLER = logging.StreamHandler()
_CONSOLE_HANDLER.setFormatter(_FORMATTER)
_LOGGER.addHandler(_CONSOLE_HANDLER)


def info(message):
    _LOGGER.info(message)


def warning(message):
    _LOGGER.warning(message)


def exception(message, exc_info):
    _LOGGER.exception(message, exc_info=exc_info)


def fatal(message, exc_info):
    _LOGGER.fatal(message, exc_info=exc_info)
