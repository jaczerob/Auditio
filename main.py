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


player = Player(use_ngrok=USE_NGROK)


def main():
    try:
        player.connect()
    except (InvalidID, ConnectionRefusedError, BrokenPipeError, ):
        logger.opt(exception=True).error('couldn\'t connect to discord, attempting re-connect in 5 seconds...')

        time.sleep(5)
        main()
        return
    else:
        logger.info('connected to discord')

    while True:
        try:
            player.update()
            if player.current_track is not None and player.current_track.exists:
                logger.trace(f'updating track={player.current_track}')
            else:
                logger.trace('no track found, rpc cleared')
                
        except struct.error:
            # ignore
            time.sleep(10)
            continue

        except (InvalidID, ConnectionRefusedError, BrokenPipeError, ):
            logger.opt(exception=True).error('lost connection to discord, attempting re-connect in 5 seconds...')
            time.sleep(5)
            main()
            return

        except Exception:
            logger.opt(exception=True).critical('unhandled exception occurred, shutting down')
            sys.exit(1)
        
        time.sleep(10)


def formatter(record) -> str:
    match record['level'].name:
        case 'ERROR':
            if record['exception']:
                return '<white>[{time}]</> <red>[{module}.{function}.{line} - {level: <8}]</> {message}\n{exception}\n'
            else:
                return '<white>[{time}]</> <red>[{module}.{function}.{line} - {level: <8}]</> {message}\n'
        case 'CRITICAL':
            if record['exception']:
                return '<white>[{time}]</> <red>[{module}.{function}.{line} - {level: <8}]</> {message}\n{exception}\n'
            else:
                return '<white>[{time}]</> <red>[{module}.{function}.{line} - {level: <8}]</> {message}\n'
        case 'TRACE':
            return '<white>[{time}] [{module: <5}]</> <blue>{level: <8}</> {message}\n'
        case _:
            return '<white>[{time}]</> <green>{level: <8}</> {message}\n'


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
        logger.info('shutting down, please wait up to 2 seconds...')
        player.disconnect()
        sys.exit(0)