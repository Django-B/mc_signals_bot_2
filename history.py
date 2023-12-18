from telethon.tl.types import InputPeerChannel
import asyncio 
import re

from db import get_messages, delete_last_messages, insert_message, init_db
from get_config import get_config
from telethon_client import user_client

from named_tuples import GameResults


config = get_config()

TARGET_CHANNEL_URL = config['target_channel_url']

async def get_round_res(message_text: str, round_num: int) -> str|None:
    '''Возвращает результат нужного раунда игры: TB, TBB, TM, TMM'''
    if not message_text:
        return None

    regex = r"{}. +[A-Z][0-9].+[A-Z].+\d\s+(?P<res>[A-Z]+)".format(str(round_num))
    res = re.search(regex, message_text)
    if res:
        print(res)
        return res.group('res')
    return None

async def get_game_results(message_text: str) -> GameResults:
    results = []
    for i in range(1, 10):
        result = await get_round_res(message_text, i)
        results.append(result)

    return GameResults(*results)

async def dump_channel_history(channel_url=TARGET_CHANNEL_URL):
    '''Собирает данные по всем играм с телеграм канала'''
    await init_db()

    channel_entity = await user_client.get_entity(channel_url)

    offset_id = 0
    messages_history = list(await get_messages())

    if messages_history:
        offset_id = await delete_last_messages(5)

    async for message in user_client.iter_messages(
            InputPeerChannel(channel_entity.id, channel_entity.access_hash), # type: ignore
        offset_id = offset_id, 
        # limit=100,
        reverse=True,
    ):
        game_results = await get_game_results(message.text)
        await insert_message(
            message_id=message.id,
            message_text=message.text,
            game_results=game_results
        )
        message_preview = message.text[:message.text.find('\n')]+'...' if message.text else '[Текст отсутствует]'
        print('Сохранение поста с ID {} | {} | {}'.format(message.id, message_preview, game_results))

async def main():
    await dump_channel_history()


if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
