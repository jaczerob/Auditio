import subprocess
import sys
import threading
import time

import rumps
from pypresence.exceptions import InvalidID

from music import get_current_track
from rpc import RPC


def exception_handler(exc_type, exc_value, exc_traceback):
    """Warn the user an exception has occurred"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    elif issubclass(exc_type, (InvalidID, KeyError)):
        rumps.alert(title='Please set a valid client ID.', message='Opening config file.')
        subprocess.call(['open', '-a', 'TextEdit', './Resources/config.ini'])
        return

    rumps.alert(title=exc_type.__name__, message=str(exc_value))


sys.excepthook = exception_handler


class App(rumps.App):
    def __init__(self, name, title=None, icon=None, template=None, menu=None, quit_button=None):
        super().__init__(name, title=title, icon=icon, template=template, menu=menu, quit_button=quit_button)
        self._rpc = RPC()
        self._update_thread = None

    @rumps.clicked('Start')
    def start(self, _):
        if self._rpc.is_connected:
            return

        self._rpc.connect()

        def update_rpc():
            while self._rpc.is_connected:
                self._rpc.update(get_current_track())
                time.sleep(15)

        update_thread = threading.Thread(target=update_rpc)
        update_thread.start()
        self._update_thread = update_thread

        rumps.notification('Apple Music RPC', 'Status', 'Running', icon='./Resources/icon.png')

    @rumps.clicked('Stop')
    def stop(self, _):
        self._close()
        rumps.notification('Apple Music RPC', 'Status', 'Stopped', icon='./Resources/icon.png')

    @rumps.clicked('Quit')
    def quit(self, _):
        self._close()
        rumps.quit_application(_)

    def _close(self):
        def clean_up():
            if not self._rpc.is_connected:
                return

            self._rpc.stop()

            if self._update_thread:
                self._update_thread.join()

        close_thread = threading.Thread(target=clean_up)
        close_thread.start()

