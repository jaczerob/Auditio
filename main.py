import asyncio
import logging, logging.config
import struct
import sys
from concurrent.futures import ThreadPoolExecutor

from pyee import AsyncIOEventEmitter
from pypresence import AioPresence
from pypresence.exceptions import InvalidID

from config import config
from track import Track
from player import Player
import process


executor = ThreadPoolExecutor(max_workers=3)

rpc = AioPresence(config['client']['id'])
ee = AsyncIOEventEmitter()
player = Player(executor)

logging.config.fileConfig('config/logging.ini', disable_existing_loggers=True)
logger = logging.getLogger('amrpc')


async def mainloop():
    while True:
        if all((
            await process.process_is_running('discord', executor),
            await process.process_is_running('music', executor)
        )):
            await poll_for_song()
        else:
            ee.emit('clear_presence', 'Discord or Music not running')
        
        await asyncio.sleep(config['music']['interval'])


async def poll_for_song():
    await player.update()

    if player.current_track.exists:
        ee.emit('update_presence', player.current_track)
    else:
        ee.emit('clear_presence', 'No track found')


@ee.on('update_presence')
async def on_update_presence(track: Track):
    await rpc.update(
        details=f'Playing {track.name}',
        state=f'by {track.artist}',
        start=track.start,
        end=track.end,
        large_image=track.album_cover,
        large_text=track.album if len(track.album) > 2 else None,
        buttons=[{'label': 'Source', 'url': 'https://github.com/thewallacems/apple-music-rpc'}],
    )

    logger.debug(f'Updated presence: {track}')


@ee.on('clear_presence')
async def on_clear_presence(reason: str):
    await rpc.clear()
    logger.debug(reason)


@ee.on('error')
async def on_error(error):
    if isinstance(error, (SystemExit, struct.error, )):
        return

    logger.exception(error)

    if isinstance(error, (InvalidID, ConnectionRefusedError, )):
        await process.restart_process()
    else:
        logging.fatal(f'Exiting out with exception: {error}')
        sys.exit(1)
    

async def main():
    await rpc.connect()
    logger.info('Connected to Discord')

    await mainloop()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except ConnectionRefusedError:
        # discord isn't open
        asyncio.run(process.wait_for_process('discord'))
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
