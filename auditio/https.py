from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urljoin, quote_plus
import glob
import os
import threading

from loguru import logger
from pyngrok import ngrok, conf
import yaml


ngrok_config_path = Path('./config/ngrok.yaml')
if not ngrok_config_path.exists():
    raise FileNotFoundError('Please see the README on how to set up album covers!')


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory='share', **kwargs)

    def do_GET(self) -> None:
        self.send_response(200)

        self.send_header('Content-Type', 'image/jpeg')
        self.end_headers()

        with open(f'share{self.path}', 'rb') as file:
            self.copyfile(file, self.wfile)

        logger.trace(f'{self.client_address[0]}:{self.client_address[1]} - "GET {self.path} {self.protocol_version}" 200')

    def log_message(self, format: str, *args) -> None:
        return


class AlbumCoverServer:
    def __init__(self) -> None:
        self.__http_server = HTTPServer(('', 8000), Handler)
        self.__http_tunnel: ngrok.NgrokTunnel = None
        self.__pyngrok_config: conf.PyngrokConfig = None

    def start(self) -> None:
        http_server_thread = threading.Thread(target=self.__http_server.serve_forever, args=(2, ))
        http_server_thread.start()
        logger.trace('http server connected on {}:{}', self.__http_server.server_address[0], self.__http_server.server_port)

        with open(ngrok_config_path, 'r') as file:
            self.__pyngrok_config = pyngrok_config = conf.PyngrokConfig(**yaml.load(file, yaml.FullLoader))

        share_path = Path('./share/').absolute()
        if not share_path.exists():
            logger.trace('creating share folder')
            share_path.mkdir()

        self.__http_tunnel: ngrok.NgrokTunnel = ngrok.connect(8000, pyngrok_config=pyngrok_config)
        logger.trace('ngrok http tunnel connected to {}', self.__http_tunnel.public_url)

    def shutdown(self) -> None:
        self.__http_server.shutdown()
        logger.trace('http server disconnected')

        ngrok.disconnect(self.__http_tunnel.public_url, pyngrok_config=self.__pyngrok_config)
        logger.trace('ngrok http tunnel disconnected')

    def get_album_cover_url(self, album: str):
        filename = quote_plus(album) + '.jpg'
        os.rename('./share/albumcover.jpg', f'./share/{filename}')

        files = glob.glob('./share/*.jpg')
        for file in files:
            if not file.endswith(filename):
                os.remove(file)
                logger.trace('removing {}', file)
                break

        url = urljoin(self.__http_tunnel.public_url, filename)
        return url
