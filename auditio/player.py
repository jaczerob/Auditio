from typing import Any
from pypresence import Presence
import yaml

from auditio.https import AlbumCoverServer
from auditio.track import Track


with open('config/config.yaml', 'r') as file:
    config: dict[str, Any] = yaml.load(file, Loader=yaml.FullLoader)


class Player:
    def __init__(self, *, use_ngrok=False) -> None:
        self.current_track: Track = None

        self.__connected = False
        self.__rpc = Presence(config['client']['id'])

        if use_ngrok:
            self.__album_cover_server = AlbumCoverServer()
        else:
            self.__album_cover_server = None

        self.__album_cover_server_connected = False

    def connect(self):
        if self.__connected:
            return
            
        self.__rpc.connect()
        self.__connected = True

        if self.__album_cover_server_connected:
            return

        if self.__album_cover_server is not None:
            self.__album_cover_server.start()
            self.__album_cover_server_connected = True

    def disconnect(self):
        if not self.__connected:
            return

        self.__rpc.close()
        self.__connected = False

        if not self.__album_cover_server_connected:
            return

        if self.__album_cover_server is not None:
            self.__album_cover_server.shutdown()

    def reconnect(self):
        if not self.__connected:
            raise ConnectionError('must connect to the player first')

        self.disconnect()
        self.connect()

    def update(self):
        if not self.__connected:
            raise ConnectionError('must connect to the player first')

        self.current_track = track = Track()

        if not track.exists:
            self.__rpc.clear()
        else:
            if self.__album_cover_server is not None:
                album_cover = self.__album_cover_server.get_album_cover_url(track.album) if track.album is not None else config['client']['default_image'] 
            else:
                album_cover = config['client']['default_image'] 

            self.__rpc.update(
                details=f'Playing {track.name}',
                state=f'by {track.artist}',
                start=track.start,
                end=track.end,
                large_image=album_cover,
                large_text=track.album,
                buttons=[{'label': 'Source', 'url': 'https://github.com/jaczerob/Auditio'}],
            )
