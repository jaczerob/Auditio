from typing import Optional

from pypresence import Presence

import config
import logger
import music

_CONNECTED = False
_RPC: Optional[Presence] = None


def update():
    if not is_connected():
        return

    track = music.get_current_track()

    if track:
        logger.info(
            f'Got Track(name={track.trackName}, artist={track.trackArtist}, position={track.trackPosition}, duration={track.trackDuration})')
        _RPC.update(state=track.state, details=track.details, large_image='icon', large_text=track.details)
        logger.info(
            f'Updated RPC(state={track.state}, details={track.details}, large_image=icon, large_text={track.details})')
    else:
        logger.info('No track found, clearing RPC')
        _RPC.clear()


def is_connected():
    return _CONNECTED


def connect():
    if is_connected():
        return

    global _RPC
    global _CONNECTED

    client_id = config.get('RPC', 'clientid', fallback=None)

    rpc = Presence(client_id)
    rpc.connect()

    _RPC = rpc
    _CONNECTED = True

    logger.info('RPC connected')


def stop():
    if not is_connected():
        return

    global _CONNECTED

    _RPC.clear()
    _RPC.close()
    _CONNECTED = False

    logger.info('RPC disconnected')
