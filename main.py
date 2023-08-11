import asyncio
import aiofiles
import sys
import argparse

from datetime import datetime


async def write_chat(args):
    reader, writer = await asyncio.open_connection(args.host, args.port)
    while True:
        record = await reader.readline()
        message = f"[{datetime.now().strftime('%d.%m.%y %I:%M')}] {record.decode('utf-8')}"
        async with aiofiles.open(args.path, 'a', encoding='utf-8') as file:
            await file.write(message)
        sys.stdout.write(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', '--host', default='minechat.dvmn.org', help='enable logging')
    parser.add_argument('-port', '--port', default='5000', help='enable delay')
    parser.add_argument('-history', '--history', default='mine_chat.history', help="History chat's file.")
    args = parser.parse_args()
    try:
        asyncio.run(write_chat(args))
    except Exception as err:
        sys.stderr.write(err)


if __name__ == '__main__':
    main()
