import asyncio
import logging, logging.config
import os
import struct
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import psutil
from pyee import AsyncIOEventEmitter
from pypresence import AioPresence
from pypresence.exceptions import InvalidID

from config import config
from music import Track, get_current_track


executor = ThreadPoolExecutor(max_workers=3)

rpc = AioPresence(config['client']['id'])
ee = AsyncIOEventEmitter()

logging.config.fileConfig('logging.ini', disable_existing_loggers=True)
logger = logging.getLogger('amrpc')


async def mainloop():
    while True:
        if all((
            await process_is_running('discord'),
            await process_is_running('music')
        )):
            await poll_for_song()
        else:
            ee.emit('clear_presence', 'Discord or Music not running')
        
        await asyncio.sleep(config['music']['interval'])


async def process_is_running(name: str) -> bool:
    def inner_func():
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['name'])
                if name.lower() in pinfo['name'].lower():
                    return True
            except:
                pass
        return False
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, inner_func)


async def restart_process():
    args = [sys.executable] + sys.argv
    subprocess.Popen(args)
    await asyncio.sleep(5)
    sys.exit('Restarting process')


async def wait_for_process(name: str) -> None:
    while not await process_is_running(name):
        logger.debug(f'Waiting for {name}...')
        await asyncio.sleep(5)


async def poll_for_song():
    if track := await get_current_track(executor=executor):
        ee.emit('update_presence', track)
    else:
        ee.emit('clear_presence', 'No track found')


@ee.on('update_presence')
async def on_update_presence(track: Track):
    await rpc.update(
        details=track.artist,
        state=track.name,
        start=track.start,
        end=track.end,
        large_image=config['client']['large_image'],
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
        await restart_process()
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
        asyncio.run(wait_for_process('discord'))
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
