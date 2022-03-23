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

from auditio import process, rpc
from auditio.track import Track


def main():
    while True:
        if all((
            process.process_is_running('discord'),
            process.process_is_running('music')
        )):
            try:
                track = Track(use_ngrok=USE_NGROK)
                rpc.update(track)
            except Exception as exc:
                handle_exception(exc)

        time.sleep(10)


def handle_exception(error):
    if isinstance(error, (SystemExit, struct.error, )):
        return

    if isinstance(error, (InvalidID, ConnectionRefusedError, )):
        process.restart_process()
    else:
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()

    logger.add(sys.stderr, level='ERROR', format='<black>[{time}] [{module}.{function}.{line}]</> <red>{level} - {exception}</> {message}')

    if args.v:
        logger.add(sys.stdout, level='TRACE', format='<black>[{time}] [{module}]</> <blue>{level}</> {message}')
    else:
        logger.add(sys.stdout, level='INFO', format='<black>[{time}]</> <green>{level}</> {message}')

    try:
        main()
    except ConnectionRefusedError:
        process.wait_for_process('discord')
        main()
    except KeyboardInterrupt:
        sys.exit(0)