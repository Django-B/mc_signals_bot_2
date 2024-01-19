from telethon.tl.types import InputPeerChannel
import asyncio 
import re

from db import get_messages, delete_last_messages, insert_message, init_db
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
        print(res)
        return res.group('res')
    return None

'''
async def get_game_results(message_id: int, message_text: str) -> Game | None:
    # Здесь должен быть код, который извлекает все данные игры
    nums_totals = await ext.extract_nums_totals(message_text)
    rounds_data = [await ext.extract_round_data(message_text, x) for x in range(1, 10)]
    try: 
        game = Game(
            message_id=message_id,
            game_date=(await ext.extract_date_and_time(message_text))[0],
            game_time=(await ext.extract_date_and_time(message_text))[1],
            p1_name=(await ext.extract_p_names(message_text))[0],
            p2_name=(await ext.extract_p_names(message_text))[1],
            p1_game_win_coef=(await ext.extract_p_game_win_coefs(message_text))[0],
            p2_game_win_coef=(await ext.extract_p_game_win_coefs(message_text))[1],
            p1_round_win_coef=(await ext.extract_p_round_win_coefs(message_text))[0],
            p2_round_win_coef=(await ext.extract_p_round_win_coefs(message_text))[1],
            f_coef=(await ext.extract_fbr(message_text))[0],
            b_coef=(await ext.extract_fbr(message_text))[1],
            r_coef=(await ext.extract_fbr(message_text))[2],
            min_num_total=nums_totals[0][0],
            min_num_total_min_coef=nums_totals[0][1],
            min_num_total_max_coef=nums_totals[0][2],
            mid_num_total=nums_totals[1][0],
            mid_num_total_min_coef=nums_totals[1][1],
            mid_num_total_max_coef=nums_totals[1][2],
            max_num_total=nums_totals[2][0],
            max_num_total_min_coef=nums_totals[2][1],
            max_num_total_max_coef=nums_totals[2][2],
            fyes=(await ext.extract_f(message_text))[0],
            fno=(await ext.extract_f(message_text))[1],
            p1_wins=(await ext.extract_p_wins(message_text))[0],
            p2_wins=(await ext.extract_p_wins(message_text))[1],
            round1_winner=rounds_data[0]['winner'],
            round1_finish=rounds_data[0]['finish'],
            round1_time=rounds_data[0]['time'],
            round1_total=rounds_data[0]['total'],
            
            round2_winner=rounds_data[1]['winner'],
            round2_finish=rounds_data[1]['finish'],
            round2_time=rounds_data[1]['time'],
            round2_total=rounds_data[1]['total'],
            
            round3_winner=rounds_data[2]['winner'],
            round3_finish=rounds_data[2]['finish'],
            round3_time=rounds_data[2]['time'],
            round3_total=rounds_data[2]['total'],
            
            round4_winner=rounds_data[3]['winner'],
            round4_finish=rounds_data[3]['finish'],
            round4_time=rounds_data[3]['time'],
            round4_total=rounds_data[3]['total'],
            
            round5_winner=rounds_data[4]['winner'],
            round5_finish=rounds_data[4]['finish'],
            round5_time=rounds_data[4]['time'],
            round5_total=rounds_data[4]['total'],
            
            round6_winner=rounds_data[5]['winner'],
            round6_finish=rounds_data[5]['finish'],
            round6_time=rounds_data[5]['time'],
            round6_total=rounds_data[5]['total'],
            
            round7_winner=rounds_data[6]['winner'],
            round7_finish=rounds_data[6]['finish'],
            round7_time=rounds_data[6]['time'],
            round7_total=rounds_data[6]['total'],
            
            round8_winner=rounds_data[7]['winner'],
            round8_finish=rounds_data[7]['finish'],
            round8_time=rounds_data[7]['time'],
            round8_total=rounds_data[7]['total'],

            round9_winner=rounds_data[8]['winner'],
            round9_finish=rounds_data[8]['finish'],
            round9_time=rounds_data[8]['time'],
            round9_total=rounds_data[8]['total'],
        )
    except TypeError: 
        return None

    return game
'''

async def dump_channel_history(channel_url=TARGET_CHANNEL_URL):
    '''Собирает данные по всем играм с телеграм канала'''
    await init_db()

    channel_entity = await user_client.get_entity(channel_url) 

    offset_id = 0
    messages_history = list(await get_messages())

    if messages_history:
        offset_id = await delete_last_messages(3)

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
        '''
        await insert_message(
            message_id=message.id,
            message_text=message.text,
            game_results=game_results
        )
        '''
        message_preview = message.text[:message.text.find('\n')]+'...' if message.text else '[Текст отсутствует]'
        # print('Сохранение поста с ID {} | {} | {}'.format(message.id, message_preview, game))
        print(message.raw_text, game)
        exit()

async def main():
    await dump_channel_history()


if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
