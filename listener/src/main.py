__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

import asyncio
from datetime import datetime
import json
from typing import Any, NoReturn

from fast_depends import inject
from loguru import logger
from telethon import TelegramClient
from telethon.events import MessageEdited, MessageDeleted, NewMessage

from opensearch import OpenSearchClient
from settings import TelegramSettings
from constants import INDEX_NAME
from base64 import b64encode


def to_dict(obj: Any) -> dict[str, Any]:
    if hasattr(obj, 'to_dict'):
        obj: dict[str, Any] = obj.to_dict()
    if isinstance(obj, dict):
        obj = {k: to_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        obj = [to_dict(o) for o in obj]
    if isinstance(obj, bytes):
        obj = b64encode(obj).decode('utf-8')
    if isinstance(obj, datetime):
        obj = str(obj)
    return obj


@inject
async def create_index(db: OpenSearchClient) -> None:
    try:
        body = {
            'settings': {
                'index': {
                    'number_of_shards': 4
                }
            }
        }
        await db.create_index(INDEX_NAME, body=body)
    except Exception as ex:
        logger.exception(ex)


@inject
async def save_message(event: NewMessage.Event | MessageEdited.Event, db: OpenSearchClient) -> None:
    try:
        chat = await event.get_chat()
        sender = await event.get_sender()
        doc = {
            'message': to_dict(event.message),
            'sender': to_dict(sender),
            'chat': to_dict(chat),
            'stringify': event.stringify(),
        }
        await db.add_document(INDEX_NAME, doc)
    except Exception as ex:
        logger.exception(ex)
        logger.error(event)


async def main() -> NoReturn:
    settings = TelegramSettings()

    async with TelegramClient('telegram-listener', settings.api_id, settings.api_hash) as client:
        client.add_event_handler(save_message, NewMessage())
        client.add_event_handler(save_message, MessageEdited())

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
