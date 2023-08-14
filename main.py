import asyncio
import os

import aiofiles
import sys
import argparse
import time
import logging
import json

from datetime import datetime
from dotenv import load_dotenv
from textwrap import dedent


logger = logging.getLogger(__name__)


class InvalidToken(Exception):
    pass


async def send_message(args, token):
    reader, writer = await asyncio.open_connection(args.host, 5050)
    response_in_bytes = await reader.readline()
    response = response_in_bytes.decode("utf-8")
    logger.debug(f'sender: {response}')
    logger.debug(f'user: {token}')
    writer.write(f"{token}\n".encode())
    await writer.drain()
    response_in_bytes = await reader.readline()
    response = json.loads(response_in_bytes.decode())
    logger.debug(f'sender: {response}')
    if response is None:
        writer.close()
        await writer.wait_closed()
        logger.debug("Token error.")
    else:
        print('good autorization')
        return




async def old_send_message(args, token):
    reader, writer = await asyncio.open_connection(args.host, args.port)
    try:
        response_in_bytes = await reader.read(1024)
        response = response_in_bytes.decode('utf-8')
        logger.debug(f'sender: {response}')
        print(response)
        message = f'{token}\r\n'
        logger.debug(f'user: {message}')
        writer.write(message.encode('utf-8'))
        await writer.drain()
        print(response)
        time.sleep(2)
        response_in_bytes = await reader.read(1024)
        response = response_in_bytes.decode("utf-8")
        logger.debug(f'sender: {response}')
        if response == '\n':
            logger.warning(dedent(f'''
                    Неизвестный токен: {token}
                    Проверьте его или зарегистрируйте заново.
                    '''))
        else:
            message = '3-я попытка\r\n\n'
            logger.debug(f'user: {message}')
            writer.write(message.encode('utf-8'))
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
    logger.setLevel(logging.DEBUG)
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

    asyncio.run(send_message(args, chat_token))




if __name__ == '__main__':
    main()
