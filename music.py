import re
import subprocess
from typing import Optional

_TRACK_REGEX = r'trackName:(.+), trackArtist:(.+), trackPosition:([0-9]+), trackDuration:([0-9]+)'
_TRACK_SCRIPT_ARGS = ['osascript', './Resources/getTrack.scpt']
_TRACK_KEYS = ['trackName', 'trackArtist', 'trackPosition', 'trackDuration']


class Track:
    def __init__(self, trackName, trackArtist, trackPosition, trackDuration):
        self.trackName = trackName
        self.trackArtist = trackArtist

        self.trackPosition = int(trackPosition)
        self.trackDuration = int(trackDuration)

    @property
    def state(self) -> str:
        position_minutes, position_seconds = divmod(self.trackPosition, 60)
        duration_minutes, duration_seconds = divmod(self.trackDuration, 60)
        state = '%02d:%02d/%02d:%02d' % (position_minutes, position_seconds, duration_minutes, duration_seconds)
        return state

    @property
    def details(self) -> str:
        return f'{self.trackArtist} - {self.trackName}'


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
