from telethon.sync import TelegramClient
from get_config import get_config
import asyncio

config = get_config()

API_ID = config['api_id']
API_HASH = config['api_hash']

loop = asyncio.get_event_loop()
user_client = TelegramClient('user', API_ID, API_HASH, loop=loop).start() # type: ignore
