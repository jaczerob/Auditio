import asyncio
import logging, logging.config
import sys
from concurrent.futures import ThreadPoolExecutor

import psutil
from pyee import AsyncIOEventEmitter
from pypresence import AioPresence

from config import config
from music import Track, get_current_track


class RPC(AioPresence):
    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()

        for task in asyncio.all_tasks(self.loop):
            try:
                task.cancel()
            except:
                pass


executor = ThreadPoolExecutor(max_workers=3)

rpc = RPC(config['client']['id'])
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
async def on_error(message):
    logger.exception(message)
    sys.exit(1)
    

async def main():
    await rpc.connect()
    logger.info('Connected to Discord')

    await mainloop()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
