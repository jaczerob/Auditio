from time import time
import re
import subprocess

TRACK_REGEX = re.compile(r'trackName:(.+), trackArtist:(.+), trackPosition:([0-9]+), trackDuration:([0-9]+), trackAlbum:(.+)')
TRACK_KEYS = ['trackName', 'trackArtist', 'trackPosition', 'trackDuration', 'trackAlbum']


class Track:
    def __init__(self) -> None:
        self.exists: bool = False

        self.name: str = None
        self.artist: str = None
        self.album: str = None
        self.start: int = None
        self.end: int = None
        self.parse()

    def parse(self) -> None:
        track = None

        result = subprocess.run(
            ['osascript', 'scripts/getTrack.scpt'], 
            capture_output=True
        )

        if result.stdout:
            data = result.stdout.decode().strip()
            if match := TRACK_REGEX.match(data):
                track = {key: value for key, value in zip(TRACK_KEYS, match.groups())}

        if track is not None:
            self.exists = True
            self.name = track['trackName']
            self.artist = track['trackArtist']
            self.album = track['trackAlbum']
            if len(self.album) < 2:
                self.album += " Album"

            self.start = start = time() - int(track['trackPosition'])
            self.end = start + int(track['trackDuration'])

    def __str__(self) -> str:
        return f'Track({self.name}, {self.artist}, {self.album}, {self.start}, {self.end})'
