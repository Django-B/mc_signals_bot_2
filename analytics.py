import asyncio
from pprint import pprint

from db import fetch, GAME_TABLE_NAME
from named_tuples import is_equal_totals


async def get_interrupt_stat(all_games, total, round_num):
    max_length = 0
    current_length = 0
    data = {}
    async for game in all_games():
        cur_total = game[f'round{round_num}_total']
        if cur_total:
            if await is_equal_totals(total, cur_total):
                current_length += 1
            else:
                if current_length >= 2:
                    if not current_length in data:
                        for key in data.keys():
                            data[key]+=1
                        data[current_length] = 1
                            
                    
                max_length = max(max_length, current_length)
                current_length = 0
    return data

async def get_streak_count(games, key, is_equal_func, min_count=10):
    '''
        Получает стату по разным длинам серий из нужного исхода
    '''
    min_count -= 1
    serial_runs = {}
    count = 0
    async for game in games():
        if game[key]:
            if is_equal_func(game[key]):
                count += 1
            else:
                if count > min_count:
                    if count in serial_runs:
                        serial_runs[count] += 1
                    else:
                        serial_runs[count] = 1
                count = 0
    if count > min_count:
        if count in serial_runs:
            serial_runs[count] += 1
        else:
            serial_runs[count] = 1
    return serial_runs

async def get_cur_streak(last_games, key, is_equal_func=lambda x: x, cut=False):
    streak = 0
    flag = False
    for game in last_games:
        finish = game[key]
        if finish:
            flag = True
            finish = game[key]
        if is_equal_func(finish):
            if not cut:
                if not flag:
                    flag = True
                    streak += 1
                elif flag:
                    if finish=='F':
                        streak += 1
                    else: 
                        break
            else:
                cut = False
    return streak


async def get_max_streak(all_games, key, is_equal_func):
    max_length = 0
    current_length = 0
    async for game in all_games():
        val = game[key]
        if val:
            if is_equal_func(val):
                current_length += 1
            else:
                max_length = max(max_length, current_length)
                current_length = 0
    max_length = max(max_length, current_length)  # Обработка случая, когда серия заканчивается в конце списка
    return max_length

async def max_f_streak(games, round_num):
    max_length = 0
    current_length = 0
    async for game in games():
        finish = game[f'round{round_num}_finish']
        if finish:
            if finish=='F':
                current_length += 1
                # b.append(game[f'round{round_num}_total'])
            else:
                max_length = max(max_length, current_length)
                # if current_length>1:
                    # print(b, current_length)
                    # b = []
                current_length = 0
    max_length = max(max_length, current_length)  # Обработка случая, когда серия заканчивается в конце списка
    return max_length

async def cur_f_streak(games_reversed, round_num: int = 1, cut: bool = False):
    '''Возвращает длину последней серии тоталов(TB, TM) в нужном раунде последних игр'''
    finish_key_name = f'round{round_num}_finish'
    cur_total = None
    streak = 0
    flag = False
    for game in games_reversed:
        finish = game[f'round{round_num}_finish']
        if finish:
            cur_total = finish
            flag = True
            finish = game[finish_key_name]
        if finish:
            if not cut:
                if not flag:
                    cur_total = finish
                    flag = True
                    streak += 1
                elif flag:
                    if finish=='F':
                        streak += 1
                    else: 
                        break
            else:
                cut = False
    return streak

async def _get_5prev_games(id_, p_name):
    '''Возвращает 5 последних игр конкретного персонажа'''
    query = f"SELECT * FROM {GAME_TABLE_NAME}\
            WHERE (p1_name='{p_name}' or p2_name='{p_name}') and id<{id_}\
            ORDER BY id DESC\
            LIMIT 5"
    games = await fetch(query)
    return list(games)


async def _get_total(games, round_num):
    '''Возвращает общий тотал 5 игр, если его нет то None'''
    totals = [x[f'round{round_num}_total'] for x in games]
    
    target_totals = ['TB', 'TM']
    # tb_res = [ all([ await is_equal_totals(target_total, x) for x in totals ]) for target_total in target_totals]
    tb_res = []
    for target_total in target_totals:
        inner_list = []
        for x in totals:
            inner_list.append(await is_equal_totals(target_total, x))
        tb_res.append(all(inner_list))
    if True in tb_res:
        return target_totals[tb_res.index(True)]
    else:
        return None

async def match_games(game, round_num):
    '''Сравнивает тотал последних 5 игр двух игроков текущей игры'''
    p1_games = await _get_5prev_games(game['id'], game['p1_name']) 
    p2_games = await _get_5prev_games(game['id'], game['p2_name']) 
    if len(p1_games)<5 or len(p2_games)<5:
        return None

    p1_total = await _get_total(p1_games, round_num)
    p2_total = await _get_total(p2_games, round_num)

    return p1_total if p1_total == p2_total else None

async def ochka_stat(all_games, round_num=1):

    data = {}
    async for game in all_games:
        game_total = game[f'round{round_num}_total']
        games_total = await match_games(game, round_num)
        if games_total:
            key = game['p1_name']+'-'+game['p2_name']
            if not key in data.keys():
                data[key] = {}
            if not game_total in data[key].keys():
                data[key][game_total] = {}
            if not games_total in data[key][game_total].keys():
                data[key][game_total][games_total] = 0
            data[key][game_total][games_total]+=1
    return data


async def main():
    from db import get_many_games
    await get_interrupt_stat(get_many_games)

if __name__ == "__main__":
    asyncio.run(main())
