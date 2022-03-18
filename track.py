from concurrent.futures import ThreadPoolExecutor
from time import time
import asyncio
import os, os.path
import re
import subprocess

from pathvalidate import sanitize_filename
import cloudinary, cloudinary.uploader
import yaml

from config import config


TRACK_REGEX = re.compile(config['music']['regex'])
TRACK_KEYS = ['trackName', 'trackArtist', 'trackPosition', 'trackDuration', 'trackAlbum']
USE_ALBUM_COVER = config['music']['album_cover']

if USE_ALBUM_COVER:
    with open('config/cloudinary.yaml', 'r') as file:
        cloudinary_config = yaml.load(file, Loader=yaml.FullLoader)
        cloudinary.config(**cloudinary_config)


class Track:
    def __init__(self, executor: ThreadPoolExecutor) -> None:
        self.exists: bool = False

        self.name: str = None
        self.artist: str = None
        self.album: str = None
        self.album_cover: str = None
        self.start: int = None
        self.end: int = None

        self.executor: ThreadPoolExecutor = executor

    async def delete(self):
        if not USE_ALBUM_COVER:
            return

        if self.album_cover == config['client']['large_image']:
            return

        def inner_func():
            public_id = (str(sanitize_filename(self.album))).replace(' ', '_')
            cloudinary.uploader.destroy(public_id)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self.executor, inner_func)
        

    async def parse(self) -> None:
        await self.__get_track_data()
        await self.__get_album_cover()

    async def __get_track_data(self) -> None:
        def inner_func():
            result = subprocess.run(
                ['osascript', 'scripts/getTrack.scpt'], 
                capture_output=True
            )

            if not result.stdout:
                return None

            data = result.stdout.decode().strip()
            if not (match := TRACK_REGEX.match(data)):
                return None

            return {key: value for key, value in zip(TRACK_KEYS, match.groups())}

        loop = asyncio.get_event_loop()
        track = await loop.run_in_executor(self.executor, inner_func)

        if track is not None:
            self.exists = True
            self.name = track['trackName']
            self.artist = track['trackArtist']
            self.album = track['trackAlbum']
            self.start = start = time() - int(track['trackPosition'])
            self.end = start + int(track['trackDuration'])
        
    async def __get_album_cover(self) -> None:
        if not USE_ALBUM_COVER:
            return config['client']['large_image']

        def inner_func():
            subprocess.run(
                ['osascript', 'scripts/getArt.scpt'], 
                capture_output=True
            )

            if not os.path.exists('tmp.jpg'):
                return None

            filename = (str(sanitize_filename(self.album)) + '.jpg').replace(' ', '_')
            os.rename('tmp.jpg', filename)

            resp = cloudinary.uploader.upload(
                filename,
                public_id=filename[:-4],
                use_filename=True,
                unique_filename=False,
            )

            os.remove(filename)
            return str(resp['secure_url'])

        loop = asyncio.get_event_loop()
        album_cover = await loop.run_in_executor(self.executor, inner_func)
        self.album_cover = album_cover or config['client']['large_image']

    def __eq__(self, other) -> bool:
        return self.album_cover == other.album_cover

    def __str__(self) -> str:
        return f'Track({self.name}, {self.artist}, {self.album}, {self.album_cover}, {self.start}, {self.end})'
