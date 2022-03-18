from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging
import subprocess
import sys

import psutil

logger = logging.getLogger('amrpc')


async def process_is_running(name: str, executor: ThreadPoolExecutor) -> bool:
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