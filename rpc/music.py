import re
import subprocess
from typing import Optional

_TRACK_REGEX = r'trackName:(.+), trackArtist:(.+), trackPosition:([0-9]+), trackDuration:([0-9]+)'
_TRACK_SCRIPT_ARGS = ['osascript', 'getTrack.scpt']
_TRACK_KEYS = ['trackName', 'trackArtist', 'trackPosition', 'trackDuration']


class Track:
    # Ignore that the args are camelcase, it's how the script I made to get the data from the track
    # returns the data and it's just easier to do this with dict unpacking, see _TRACK_REGEX or
    # _getTrack.scpt
    def __init__(self, trackName, trackArtist, trackPosition, trackDuration):
        self._track_name = trackName
        self._track_artist = trackArtist

        self._track_position = int(trackPosition)
        self._track_duration = int(trackDuration)

    @property
    def state(self) -> str:
        position_minutes, position_seconds = divmod(self._track_position, 60)
        duration_minutes, duration_seconds = divmod(self._track_duration, 60)
        state = f'{position_minutes}:{position_seconds:02d}/{duration_minutes}:{duration_seconds:02d}'
        return state

    @property
    def details(self) -> str:
        return f'{self._track_artist} - {self._track_name}'

    def __repr__(self):
        return f'Track(name={self._track_name}, artist={self._track_artist}, ' \
               f'position={self._track_position}, duration={self._track_duration})'

    def __str__(self):
        return self.__repr__()


def get_current_track() -> Optional[Track]:
    result = subprocess.run(_TRACK_SCRIPT_ARGS, capture_output=True)
    if not result.stdout:
        return None

    data = result.stdout.decode().strip()
    regex = re.compile(_TRACK_REGEX)
    if not (match := regex.match(data)):
        return None

    track = {key: value for key, value in zip(_TRACK_KEYS, match.groups())}
    return Track(**track)
