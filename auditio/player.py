from pypresence import Presence

from auditio.config import app_config
from auditio.track import Track


class Player:
    def __init__(self) -> None:
        self.__connected = False
        self.__rpc = Presence(app_config['client']['id'])

    def connect(self):
        if self.__connected:
            return
            
        self.__rpc.connect()
        self.__connected = True

    def disconnect(self):
        if not self.__connected:
            return

        self.__rpc.close()
        self.__connected = False

    def reconnect(self):
        if not self.__connected:
            raise ConnectionError('must connect to the player first')

        self.disconnect()
        self.connect()

    def update(self, track: Track):
        if not self.__connected:
            raise ConnectionError('must connect to the player first')

        self.__rpc.update(
            details=f'Playing {track.name}',
            state=f'by {track.artist}',
            start=track.start,
            end=track.end,
            large_image=track.album_cover,
            large_text=track.album,
            buttons=[{'label': 'Source', 'url': 'https://github.com/jaczerob/Auditio'}],
        )

    def clear(self):
        if not self.__connected:
            raise ConnectionError('must connect to the player first')

        self.__rpc.clear()
