import os
import asyncio
import logging

import gui

from dotenv import load_dotenv
from datetime import datetime


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w")

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


async def submit_message(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, queue: asyncio.Queue):

    status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
    while True:
        message = await queue.get()
        logger.debug(f'user: {message}')
        message = message.replace('\\n', '')
        message = f'{message}\n\n'
        writer.write(message.encode('utf-8'))
        await writer.drain()
        await reader.readline()
        # watchdog_queue.put_nowait('Message sent')


async def generate_msgs(time):
    for _ in range(1, time):
        messages_queue.put_nowait(int(datetime.now().timestamp()))
        await asyncio.sleep(1)


async def main():
    load_dotenv()
    host = os.getenv('HOST')
    port_read = os.getenv('PORT_READ')
    port_write = os.getenv('PORT_WRITE')
    name = os.getenv('NICK_NAME')
    token = os.getenv('CHAT_TOKEN')
    path = os.getenv('PATH_HISTORY')
    message = 'Hi, I am robot.'

    await asyncio.gather(
        generate_msgs(30),
        gui.draw(messages_queue, sending_queue, status_updates_queue)
    )









if __name__ == '__main__':
    loop.run_until_complete(main())
    # loop.run_until_complete(gui.draw(messages_queue, sending_queue, status_updates_queue))