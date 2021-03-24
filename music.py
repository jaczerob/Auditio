import re
import subprocess


_TRACK_REGEX = r'trackName:(.+), trackArtist:(.+), trackPosition:([0-9]+), trackDuration:([0-9]+)'
_TRACK_SCRIPT_ARGS = ['osascript', './Resources/getTrack.scpt']
_TRACK_KEYS = ['trackName', 'trackArtist', 'trackPosition', 'trackDuration']


def get_current_track():
    result = subprocess.run(_TRACK_SCRIPT_ARGS, capture_output=True)
    if not result.stdout:
        return None

    data = result.stdout.decode().strip()
    regex = re.compile(_TRACK_REGEX)
    if not (match := regex.match(data)):
        return None

    track = {key: value for key, value in zip(_TRACK_KEYS, match.groups())}
    return track
