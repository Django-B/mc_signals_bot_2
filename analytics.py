from db import fetch, GAME_TABLE_NAME
from named_tuples import is_equal_totals


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
    tb_res = [ all([ await is_equal_totals(target_total, x) for x in totals ]) for target_total in target_totals]
    print(f'{tb_res=}')
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


        
        

