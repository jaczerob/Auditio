from typing import Optional
import logging

from pypresence import Presence
from loguru import logger

from auditio.config import app_config
from auditio.track import Track


rpc = Presence(app_config['client']['id'])
rpc.connect()

logger.info('connected to discord')


def update(track: Optional[Track]):
    if track.name == None:
        logger.trace('no track found, clearing rpc')
        rpc.clear()
        return

    rpc.update(
        details=f'Playing {track.name}',
        state=f'by {track.artist}',
        start=track.start,
        end=track.end,
        large_image=track.album_cover,
        large_text=track.album,
        buttons=[{'label': 'Source', 'url': 'https://github.com/thewallacems/apple-music-rpc'}],
    )

    logger.trace(f'updated presence: {track}')


def clear():
    rpc.clear()
