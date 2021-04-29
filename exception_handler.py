import sys

import rumps
from pypresence.exceptions import InvalidID

import logger


def exception_handler(exc_type, exc_value, exc_traceback):
    """Warn the user an exception has occurred"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    message = str(exc_value)
    if issubclass(exc_type, InvalidID):
        message = 'Your client ID is invalid. Please update the client ID in Package Info > Resources > Resources > ' \
                  'config.ini '

    rumps.alert(title=exc_type.__name__, message=message, icon_path='./Resources/icon.png')
    logger.exception(message=str(exc_value), exc_info=(exc_type, exc_value, exc_traceback,))
    return


sys.excepthook = exception_handler
