import asyncio
import os

import aiofiles
import argparse
import logging
import json

from dotenv import load_dotenv


logger = logging.getLogger(__name__)


async def get_token(host, port, username):
    reader, writer = await asyncio.open_connection(host, port)

    try:
        response = await reader.readline()
        response = response.decode("utf-8")
        logger.debug(f"Message: {response}")

        skip_auth_reply = "\n"
        writer.write(skip_auth_reply.encode())
        await writer.drain()
        logger.debug(f"Answer: {skip_auth_reply}")

        response = await reader.readline()
        response = response.decode("utf-8")
        logger.debug(f"Message: {response}")

        username = username.replace('\n', ' ')
        writer.write(f"{username}\n".encode())
        await writer.drain()
        logger.debug(f"Answer: {username}")

        signup_result = await reader.readline()
        signup_result = json.loads(signup_result.decode())
        logger.debug(f"Message: {signup_result}")

        async with aiofiles.open('token.txt', 'w') as token_file:
            await token_file.write(signup_result['account_hash'])
    finally:
        writer.close()
        await writer.wait_closed()


async def send_message(host, port, token, message_text):
    token = token.replace('\n', ' ')
    message_text = message_text.replace('\n', ' ')
    reader, writer = await asyncio.open_connection(host, port)

    try:
        response_in_bytes = await reader.readline()
        response = response_in_bytes.decode("utf-8")
        logger.debug(f'sender: {response}')
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
            message = message_text.replace('\\n', '')
            message = f'{message}\n\n'
            writer.write(message.encode('utf-8'))
            await writer.drain()
            await reader.readline()
            response_in_bytes = await reader.readline()
            response = json.loads(response_in_bytes.decode())
            logger.debug(f'sender: {response}')
    finally:
        writer.close()
        await writer.wait_closed()


def main():
    logger.setLevel(logging.DEBUG)
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('-host', '--host', default='minechat.dvmn.org', help='host')
    parser.add_argument('-port', '--port', default='5050', help='write port')
    parser.add_argument('-token', '--token', help="Chat's token.")
    parser.add_argument('-name', '--name', help="Chat's user name.")
    parser.add_argument('-text', '--text', help="Message's text.")
    args = parser.parse_args()

    chat_token = os.getenv('CHAT_TOKEN')
    if args.token:
        chat_token = args.token

    if chat_token:
        asyncio.run(send_message(args.host, args.port, args.token, args.text))
    else:
        asyncio.run(get_token(args.host, args.port, args.name))


if __name__ == '__main__':
    main()
