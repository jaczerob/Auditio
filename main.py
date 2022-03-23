try:
    import auditio.https
    USE_NGROK = True
except FileNotFoundError:
    USE_NGROK = False

import argparse
import struct
import sys
import time

from pypresence.exceptions import InvalidID
from loguru import logger

from auditio.player import Player
from auditio.track import Track


def main():
    try:
        player = Player()
        player.connect()
    except (InvalidID, ConnectionRefusedError, BrokenPipeError, ):
        logger.error('couldn\'t connect to discord, attempting re-connect in 5 seconds...')
        time.sleep(5)
        main()
        return

    while True:
        try:
            track = Track(use_ngrok=USE_NGROK)
            if track.name == None:
                player.clear()
                logger.trace('no track found, clearing rpc')
            else:
                player.update(track)
                logger.trace(f'updating track={track}')
                
        except (SystemExit, struct.error, ):
            continue

        except (InvalidID, ConnectionRefusedError, BrokenPipeError, ):
            logger.error('lost connection to discord, attempting re-connect in 5 seconds...')
            time.sleep(5)
            main()
            return

        except Exception:
            logger.critical('unhandled exception occurred, shutting down')
            sys.exit(1)
        

        time.sleep(10)


def formatter(record) -> str:
    match record['level'].name:
        case 'ERROR':
            if record['exception']:
                return '<white>[{time}]</> <red>[{module}.{function}.{line} - {level}]</> {message}\n{exception}\n'
            else:
                return '<white>[{time}]</> <red>[{module}.{function}.{line} - {level}]</> {message}\n'
        case 'CRITICAL':
            if record['exception']:
                return '<white>[{time}]</> <red>[{module}.{function}.{line} - {level}]</> {message}\n{exception}\n'
            else:
                return '<white>[{time}]</> <red>[{module}.{function}.{line} - {level}]</> {message}\n'
        case 'TRACE':
            return '<white>[{time}] [{module}]</> <blue>{level}</> {message}\n'
        case _:
            return '<white>[{time}]</> <green>{level}</> {message}\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()

    logger.remove()

    if args.v:
        logger.add(sys.stderr, level='TRACE', format=formatter)
    else:
        logger.add(sys.stderr, level='INFO', format=formatter)

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)