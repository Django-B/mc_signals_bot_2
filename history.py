from telethon.tl.types import InputPeerChannel
import asyncio 
import re

from db import get_some_games, delete_last_messages, insert_message, init_db
from get_config import get_config
from telethon_client import user_client

from named_tuples import Game
import extractor as ext


config = get_config()

TARGET_CHANNEL_URL = config['target_channel_url']

async def get_round_res(message_text: str, round_num: int) -> str|None:
    '''Возвращает результат нужного раунда игры: TB, TBB, TM, TMM'''
    if not message_text:
        return None

    regex = r"{}. +[A-Z][0-9].+[A-Z].+\d\s+(?P<res>[A-Z]+)".format(str(round_num))
    res = re.search(regex, message_text)
    if res:
        logger.info(res)
        return res.group('res')
    return None


async def dump_channel_history(channel_url=TARGET_CHANNEL_URL):
    '''Собирает данные по всем играм с телеграм канала'''
    channel_entity = await user_client.get_entity(channel_url) 

    offset_id = 0
    delete_count = 10
    games = list(await get_some_games(delete_count+5)) # берем с запасом на всякий случай

    if games:
        offset_id = await delete_last_messages(delete_count)
        logger.info(f'Удалены последние {delete_count} сообщений')

    # перебор последних сообщений канала
    async for message in user_client.iter_messages(
        InputPeerChannel(channel_entity.id, channel_entity.access_hash), # type: ignore
        offset_id = offset_id,
        # limit=100,
        reverse=True,
    ):
        if not message.text: 
            continue
        # game = await get_game_results(message.id, message.text)
        game = await ext.extract_game_data(message)
        if not game:
            continue

        await insert_message(game=game)
        message_preview = message.text[:message.text.find('\n')]+'...' if message.text else '[Текст отсутствует]'
        logger.info('Сохранение поста с ID {} | {} '.format(message.id, message_preview))

async def main():
    await dump_channel_history()


if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
