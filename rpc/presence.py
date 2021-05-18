from typing import Optional

from pypresence import Presence

from rpc import config
from rpc import logger
from rpc import music

_CONNECTED = False
_RPC: Optional[Presence] = None


def update():
    if not _CONNECTED:
        return

    track = music.get_current_track()

    if track:
        logger.info(f'Got {track}')
        _RPC.update(state=track.state, details=track.details, large_image='icon', large_text=track.details)
        logger.info(
            f'Updated RPC(state={track.state}, details={track.details}, large_image=icon, large_text={track.details})')
    else:
        logger.info('No track found, clearing RPC')
        _RPC.clear()


def is_connected():
    return _CONNECTED


def connect():
    global _RPC
    global _CONNECTED

    if _CONNECTED:
        return

    client_id = config.get('RPC', 'clientid', fallback=None)

    rpc = Presence(client_id)
    rpc.connect()

    _RPC = rpc
    _CONNECTED = True

    logger.info('RPC connected')


def stop():
    global _CONNECTED

    if not _CONNECTED:
        return

    _RPC.clear()
    _RPC.close()
    _CONNECTED = False

    logger.info('RPC disconnected')
