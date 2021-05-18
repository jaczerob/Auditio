import os.path
import sys

import rumps

import rpc
from rpc.exception_handler import exception_handler


AppInstance = rumps.App('Apple Music RPC', title='AMRPC')


def update(_):
    rpc.update()


update_timer = rumps.Timer(callback=update, interval=15)


@rumps.clicked('Start')
def start(_):
    try:
        rpc.connect()
        update_timer.start()
        rumps.notification('Apple Music RPC', 'Status', 'Running', icon='AppIcon.icns')
    except:
        # Gotta figure out a better way to handle exceptions here because changing the sys.excepthook isn't working
        # for rumps
        exception_handler(*sys.exc_info())


@rumps.clicked('Stop')
def stop(_):
    try:
        rpc.stop()
        update_timer.stop()
        rumps.notification('Apple Music RPC', 'Status', 'Stopped', icon='AppIcon.icns')
    except:
        # Gotta figure out a better way to handle exceptions here because changing the sys.excepthook isn't working
        # for rumps
        exception_handler(*sys.exc_info())


@rumps.clicked('Show Log')
def show_log(_):
    log_file = 'amrpc.log'
    title = 'Log File'
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            message = file.read()
    else:
        message = 'No log found.'

    window = rumps.Window(title=title, default_text=message)
    window.icon = 'AppIcon.icns'
    window.run()
