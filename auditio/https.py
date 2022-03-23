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

        logger.trace(f'{self.client_address[0]}:{self.client_address[1]} - "GET {self.path} HTTP/{self.protocol_version}" 200')

    def log_message(self, format: str, *args) -> None:
        return


client = HTTPServer(('', 8000), Handler)
http_thread = threading.Thread(target=client.serve_forever)
http_thread.start()


with open(ngrok_config_path, 'r') as file:
    pyngrok_config = conf.PyngrokConfig(**yaml.load(file, yaml.FullLoader))


share_path = Path('./share/').absolute()
if not share_path.exists():
    logger.trace('creating share folder')
    share_path.mkdir()


http_tunnel: ngrok.NgrokTunnel = ngrok.connect(8000, pyngrok_config=pyngrok_config)
logger.trace('ngrok http tunnel connected')


def replace_old_album_cover(album: str):
    filename = quote_plus(album) + '.jpg'
    os.rename('./share/albumcover.jpg', f'./share/{filename}')

    files = glob.glob('./share/*.jpg')
    for file in files:
       if not file.endswith(filename):
            os.remove(file)
            break
    
    return filename


def get_album_cover_url(album: str):
    filename = replace_old_album_cover(album)
    url = urljoin(http_tunnel.public_url, filename)
    return url
