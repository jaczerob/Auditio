import sys

import rpc
from exception_handler import exception_handler

import rumps


def update(_):
    rpc.update()


update_timer = rumps.Timer(callback=update, interval=15)


def start():
    try:
        rpc.connect()
        update_timer.start()
    except:
        exception_handler(*sys.exc_info())


def stop():
    try:
        rpc.stop()
        update_timer.stop()
    except:
        exception_handler(*sys.exc_info())


class App(rumps.App):
    @rumps.clicked('Start')
    def start(self, _):
        start()
        rumps.notification('Apple Music RPC', 'Status', 'Running', icon='./Resources/icon.png')

    @rumps.clicked('Stop')
    def stop(self, _):
        stop()
        rumps.notification('Apple Music RPC', 'Status', 'Stopped', icon='./Resources/icon.png')

    @rumps.clicked('Quit')
    def quit(self, _):
        stop()
        rumps.quit_application(_)
