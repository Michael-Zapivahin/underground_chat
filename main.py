import os
import asyncio
import logging

import gui
import aiofiles

from dotenv import load_dotenv
from datetime import datetime


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename="log.txt", filemode="w")

loop = asyncio.get_event_loop()

messages_queue = asyncio.Queue()
sending_queue = asyncio.Queue()
status_updates_queue = asyncio.Queue()


async def connect_to_chat(host, port, token):
    message_text = 'hi hi hi hi hi'
    try:
        status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(f"{message_text}\n".encode())
        await writer.drain()
        response_in_bytes = await reader.readline()
        logger.debug(f'write message: {response_in_bytes.decode("utf-8")}')
        status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)
        messages_queue.put_nowait('Иван: Привет всем в этом чатике!')
        msg = await sending_queue.get()
        print(msg)
    except:
        logger.debug(f'connect error')
    finally:
        status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.CLOSED)


async def generate_msgs(time, queue):
    for _ in range(1, time):
        queue.put_nowait(int(datetime.now().timestamp()))
        await asyncio.sleep(1)


async def read_msgs(host, port, queue, path_chat_file):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        while True:
            record = await reader.readline()
            message = f"[{datetime.now().strftime('%d.%m.%y %I:%M')}] {record.decode('utf-8')}"
            queue.put_nowait(message)
            async with aiofiles.open(path_chat_file, 'a', encoding='utf-8') as file:
                await file.write(message)
    finally:
        writer.close()
        await writer.wait_closed()


async def save_messages(path_chat_file, queue):
    if os.path.exists(path_chat_file):
        async with aiofiles.open(path_chat_file, 'r') as file:
            all_file = await file.readlines()
            for message in all_file:
                queue.put_nowait(message)


async def send_msgs(host, port, token, msg):
    while True:
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(f"{token}\n".encode())
        await writer.drain()
        response_in_bytes = await reader.readline()
        response = response_in_bytes.decode()
        logger.debug(f'token : {response}')

        # msg = await queue.get()
        # msg = msg.replace('\n', ' ')
        # print(msg)
        message = msg.replace('\\n', '')
        message = f'{message}\n\n'
        writer.write(message.encode('utf-8'))
        await writer.drain()
        response_in_bytes =await reader.readline()
        response = response_in_bytes.decode()
        logger.debug(f'token : {response}')


async def get_authorization(host, port, token, queue):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        response_in_bytes = await reader.readline()
        response = response_in_bytes.decode("utf-8")
        logger.debug(f'sender: {response}')
        writer.write(f"{token}\n".encode())
        await writer.drain()
        response_in_bytes = await reader.readline()
        response = response_in_bytes.decode()
        if response is None:
            writer.close()
            await writer.wait_closed()
            logger.debug("Token error.")
        else:
            logger.debug(f'authorization successful: {response}')
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    logger.setLevel(logging.DEBUG)
    load_dotenv()
    host = os.getenv('HOST')
    port_read = os.getenv('PORT_READ')
    port_write = os.getenv('PORT_WRITE')
    name = os.getenv('NICK_NAME')
    token = os.getenv('CHAT_TOKEN')
    path_chat_file = os.getenv('PATH_HISTORY')

    # await send_msgs(host, port_write, token, 'caxasvxudsxiasbd')
    await asyncio.gather(
        send_msgs(host, port_write, token, 'test send msg.'),
        # get_authorization(host, port_write, token, status_updates_queue),
        # send_msgs(host, port_write, token, sending_queue),
        read_msgs(host, port_read, messages_queue, path_chat_file),
        gui.draw(messages_queue, sending_queue, status_updates_queue),
    )


if __name__ == '__main__':
    loop.run_until_complete(main())
