import configparser

from pypresence import Presence


config = configparser.ConfigParser()
config.read('./Resources/config.ini')


class RPC:
    def __init__(self):
        self._connected = False
        self._rpc = None

    @property
    def is_connected(self):
        return self._connected

    def connect(self):
        client_id = config.get('RPC', 'clientid', fallback=None)
        if not client_id:
            raise KeyError('No clientid set.')

        rpc = Presence(client_id)
        rpc.connect()
        rpc.clear()  # Will throw InvalidID if client ID invalid

        self._rpc = rpc
        self._connected = True

    def stop(self):
        self._rpc.clear()
        self._rpc.close()
        self._connected = False

    def update(self, track):
        if track:
            position = int(track['trackPosition'])
            position_minutes, position_seconds = divmod(position, 60)

            duration = int(track['trackDuration'])
            duration_minutes, duration_seconds = divmod(duration, 60)

            details = f"{track['trackArtist']} - {track['trackName']}"
            state = '%02d:%02d/%02d:%02d' % (position_minutes, position_seconds, duration_minutes, duration_seconds)

            self._rpc.update(state=state, details=details, large_image='icon', large_text=details)
        else:
            self._rpc.clear()
