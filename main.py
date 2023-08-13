import asyncio
import os

import aiofiles
import sys
import argparse
import time

from datetime import datetime
from dotenv import load_dotenv


async def send_message(args, token):
    reader, writer = await asyncio.open_connection(args.host, args.port)
    try:
        writer.write(f'{token}\r\n'.encode('utf-8'))
        await writer.drain()
        writer.write('test message for chat\r\n\n'.encode('utf-8'))
        await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()


async def write_chat(args):
    reader, writer = await asyncio.open_connection(args.host, args.port)
    while True:
        record = await reader.readline()
        message = f"[{datetime.now().strftime('%d.%m.%y %I:%M')}] {record.decode('utf-8')}"
        async with aiofiles.open(args.path, 'a', encoding='utf-8') as file:
            await file.write(message)
        sys.stdout.write(message)


def main():
    load_dotenv()
    chat_token = os.getenv('CHAT_TOKEN')
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', '--host', default='minechat.dvmn.org', help='enable logging')
    parser.add_argument('-port', '--port', default='5000', help='enable delay')
    parser.add_argument('-history', '--history', default='mine_chat.history', help="History chat's file.")
    args = parser.parse_args()
    # try:
    #     asyncio.run(write_chat(args))
    # except Exception as err:
    #     sys.stderr.write(err)
    try:
        asyncio.run(send_message(args, chat_token))
    except Exception as err:
        sys.stderr.write(err)



if __name__ == '__main__':
    main()
