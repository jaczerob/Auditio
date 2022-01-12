import asyncio
import re
import subprocess
from time import time
from typing import Optional

from config import config


regex = re.compile(config['music']['regex'])
args = ['osascript', 'getTrack.scpt']
keys = ['trackName', 'trackArtist', 'trackPosition', 'trackDuration']


class Track:
    def __init__(self, trackName, trackArtist, trackPosition, trackDuration):
        self.name = trackName
        self.artist = trackArtist
        self.start = start = time() - int(trackPosition)
        self.end = start + int(trackDuration)

    def __repr__(self):
        return f'Track(name={self.name}, artist={self.artist}, ' \
               f'start={self.start}, end={self.end})'

    def __str__(self):
        return self.__repr__()


async def get_current_track(executor=None) -> Optional[Track]:
    def inner_func():
        result = subprocess.run(args, capture_output=True)
        if not result.stdout:
            return None

        data = result.stdout.decode().strip()
        if not (match := regex.match(data)):
            return None

        track = {key: value for key, value in zip(keys, match.groups())}
        return Track(**track)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, inner_func)
    