import asyncio

import aiofiles
import sys
import argparse
import logging

from datetime import datetime
from dotenv import load_dotenv


logger = logging.getLogger(__name__)


async def save_messages(host, port, path):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        while True:
            record = await reader.readline()
            message = f"[{datetime.now().strftime('%d.%m.%y %I:%M')}] {record.decode('utf-8')}"
            async with aiofiles.open(path, 'a', encoding='utf-8') as file:
                await file.write(message)
            sys.stdout.write(message)
    finally:
        writer.close()
        await writer.wait_closed()


def main():
    logger.setLevel(logging.DEBUG)
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', '--host', default='minechat.dvmn.org', help='host')
    parser.add_argument('-port', '--port', default='5000', help='reade port')
    parser.add_argument('-history', '--history', default='mine_chat.history', help="History chat's file.")
    args = parser.parse_args()
    try:
        asyncio.run(save_messages(args.host, args.port, args.path))
    except Exception as err:
        sys.stderr.write(err)


if __name__ == '__main__':
    main()
