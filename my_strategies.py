import asyncio


from logger import logger
from named_tuples import Games
from named_tuples import cur_round_total_streak, max_round_total_streak, get_max_streak, get_cur_streak, is_equal_totals
from get_config import get_config
from analytics import match_games, ochka_stat, \
    max_f_streak, cur_f_streak,\
    get_cur_streak, get_max_streak

from db import get_some_filter_games



strategies = []

def strategy(func):
    strategies.append(func)
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
    return wrapper


def get_env_variables(total):
    config = get_config('variables')
    if total:
        total = total.lower()
        return int(config[total]) if total in config else 1
        
    return int(config[total.lower() + '_streak_limit']) if total.lower() + '_streak_limit' in config else 2 # type: ignore

@strategy
async def strategynof(last_games, all_games, all_games_rev):
    '''Не фаталити'''
    signals = []

    for round_num in range(1,6):
        key = f'round{round_num}_finish'
        last_game = ''
        for game in last_games:
            if game[key] and game[key] != 'F':
                last_game = game['game_id']
                break
        cur_streak = await get_cur_streak(last_games,key,lambda x: x!='F')
        cur_streak_cut = await  get_cur_streak(last_games,key,lambda x: x!='F', cut=True)

        if cur_streak >= get_env_variables('nof_limit'):
            signals.append(f'Серия Fаталити в {round_num}-м раунде достигла {cur_streak}')
        elif cur_streak_cut >= get_env_variables('nof_limit') and cur_streak == 1:
            signals.append(f'Серия Fаталити в {round_num}-м раунде достигла {cur_streak}✅\nhttps://t.me/statamk9/{last_game}')

        return signals



@strategy
async def strategyf(last_games, all_games, all_games_rev):
    '''Фаталити'''

    signals = []

    for round_num in range(1,6):
        last_game = ''
        for game in last_games:
            if game[f'round{round_num}_finish'] and game[f'round{round_num}_finish'] == 'F':
                last_game = game['game_id']
                break
        cur_streak = await cur_f_streak(last_games)
        cur_streak_cut = await cur_f_streak(last_games, cut=True)

        if cur_streak >= get_env_variables('f_limit'):
            signals.append(f'Серия Fаталити в {round_num}-м раунде достигла {cur_streak}')
        elif cur_streak_cut >= get_env_variables('f_limit') and cur_streak == 1:
            signals.append(f'Серия Fаталити в {round_num}-м раунде достигла {cur_streak}✅\nhttps://t.me/statamk9/{last_game}')

        return signals



@strategy
async def strategytb(last_games, all_games, all_games_rev):
    games = last_games


    signals = []
    for round_num in range(1, 6):
        last_game = ''
        for game in games:
            if game[f'round{round_num}_total']:
                last_game = game['game_id']
                break

        real_cur_streak = await cur_round_total_streak(games, round_num=round_num)
        cur_streak = await cur_round_total_streak(games, round_num=round_num)
        cur_streak2 = await cur_round_total_streak(games, round_num=round_num, cut=True)
        logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
        logger.info(f'{cur_streak.streak=}')
        logger.info(f'{cur_streak2.streak=}')
        if cur_streak.streak >= get_env_variables(cur_streak.total):
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= get_env_variables(cur_streak.total) and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals

'''
@strategy
async def strategytbb(last_games, all_games, all_games_rev):
    games = last_games

    total = 'TBB'

    signals = []
    for round_num in range(1, 6):
        last_game = ''
        for game in games:
            if game[f'round{round_num}_total']:
                last_game = game['game_id']
                break

        real_cur_streak = await cur_round_total_streak(games, round_num=round_num)
        cur_streak = await cur_round_total_streak(games, round_num=round_num, total=total)
        cur_streak2 = await cur_round_total_streak(games, round_num=round_num, total=total, cut=True)
        logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
        logger.info(f'{cur_streak.streak=}')
        logger.info(f'{cur_streak2.streak=}')
        if cur_streak.streak >= get_env_variables(total):
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= get_env_variables(total) and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals


@strategy
async def strategytbbb(last_games, all_games, all_games_rev):
    games = last_games

    total = 'TBBB'

    signals = []
    for round_num in range(1, 6):
        last_game = ''
        for game in games:
            if game[f'round{round_num}_total']:
                last_game = game['game_id']
                break

        real_cur_streak = await cur_round_total_streak(games, round_num=round_num)

        cur_streak = await cur_round_total_streak(games, round_num=round_num, total=total)
        cur_streak2 = await cur_round_total_streak(games, round_num=round_num, total=total, cut=True)
        logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
        logger.info(f'{cur_streak.streak=}')
        logger.info(f'{cur_streak2.streak=}')
        if cur_streak.streak >= get_env_variables(total):
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}') # type: ignore

        elif cur_streak2.streak >= get_env_variables(total) and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals

@strategy
async def strategytm(last_games, all_games, all_games_rev):
    games = last_games

    total = 'TM'

    signals = []
    for round_num in range(1, 6):
        last_game = ''
        for game in games:
            if game[f'round{round_num}_total']:
                last_game = game['game_id']
                break

        real_cur_streak = await cur_round_total_streak(games, round_num=round_num)
        cur_streak = await cur_round_total_streak(games, round_num=round_num, total=total)
        cur_streak2 = await cur_round_total_streak(games, round_num=round_num, total=total, cut=True)
        logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
        logger.info(f'{cur_streak.streak=}')
        logger.info(f'{cur_streak2.streak=}')
        if cur_streak.streak >= get_env_variables(total):
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= get_env_variables(total) and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals

@strategy
async def strategytmm(last_games, all_games, all_games_rev):
    games = last_games

    total = 'TMM'

    signals = []
    for round_num in range(1, 6):
        last_game = ''
        for game in games:
            if game[f'round{round_num}_total']:
                last_game = game['game_id']
                break

        real_cur_streak = await cur_round_total_streak(games, round_num=round_num)
        cur_streak = await cur_round_total_streak(games, round_num=round_num, total=total)
        cur_streak2 = await cur_round_total_streak(games, round_num=round_num, total=total, cut=True)
        logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
        logger.info(f'{cur_streak.streak=}')
        logger.info(f'{cur_streak2.streak=}')
        if cur_streak.streak >= get_env_variables(total):
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= get_env_variables(total) and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals


@strategy
async def strategytmmm(last_games, all_games, all_games_rev):
    games = last_games

    total = 'TMMM'

    signals = []
    for round_num in range(1, 6):
        last_game = ''
        for game in games:
            if game[f'round{round_num}_total']:
                last_game = game['game_id']
                break

        real_cur_streak = await cur_round_total_streak(games, round_num=round_num)
        cur_streak = await cur_round_total_streak(games, round_num=round_num, total=total)
        cur_streak2 = await cur_round_total_streak(games, round_num=round_num, total=total, cut=True)
        logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
        logger.info(f'{cur_streak.streak=}')
        logger.info(f'{cur_streak2.streak=}')
        if cur_streak.streak >= get_env_variables(total):
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= get_env_variables(total) and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals
'''



'''
@strategy
async def strategy_players_tb(last_games, all_games, all_games_rev):
    total = 'TB'

    last_game = last_games[0]
    p1 = last_game['p1_name']
    p2 = last_game['p2_name']

    p1_games = (await get_some_filter_games(-6, 'p1_name', p1))\
            [1:]
    p2_games = (await get_some_filter_games(-6, 'p2_name', p2))\
            [1:]

    p1_p2_games = p1_games+p2_games
    is_true = all([(await is_equal_totals(total, x['round1_total'])) for x in p1_p2_games])
    if is_true:
        last_game_id = last_game['game_id']
        return f'Сигнал на очку {p1} и {p2}, тотал {total}\nhttps://t.me/statamk10/{last_game_id}'
'''

'''
@strategy
async def strategy_players_tm(last_games, all_games, all_games_rev):
    res = []
    for total in ('TM', 'TB'):
        all_total = await match_games(last_games[0], round_num=1)
        last_game_id = last_games[0]['id']
        if all_total:
            if all_total == total:
                res.append(f'Двойная серия {all_total}\nhttps://t.me/statamk10/{last_game_id}')
    return res
'''




'''
@strategy
async def strategy_ochka(last_games, all_games, all_games_rev):
    last_game = last_games[0]
    p1 = last_game['p1_name']
    p2 = last_game['p2_name']
    
'''




'''
@strategy
async def strategy6(last_games, all_games, all_games_rev):
    val = 'TB'
    round1_num, round2_num = 1, 2
    games_reversed = last_games
    last_game = games_reversed[0]['game_id']
    async def cur_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game[total1_key_name]
            total2 = game[total2_key_name]
            if total1 and total2:
                if total1.startswith(val) and total2.startswith(val):
                    streak += 1
                else: 
                    break
            else:
                return False
        return streak
    async def max_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_streak = 0
        max_streak = 0

        async for game in all_games():
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val) and \
                game[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    # max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy7(last_games, all_games, all_games_rev):
    val = 'TB'
    round1_num, round2_num = 2, 3
    games_reversed = last_games
    last_game = games_reversed[0]['game_id']
    async def cur_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game[total1_key_name]
            total2 = game[total2_key_name]
            if total1 and total2:
                if total1.startswith(val) and total2.startswith(val):
                    streak += 1
                else: 
                    break
            else:
                return False
        return streak
    async def max_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_streak = 0
        max_streak = 0

        async for game in all_games():
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val) and \
                game[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    # max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy8(last_games, all_games, all_games_rev):
    val = 'TM'
    round1_num, round2_num = 1, 2
    games_reversed = last_games
    last_game = games_reversed[0]['game_id']
    async def cur_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game[total1_key_name]
            total2 = game[total2_key_name]
            if total1 and total2:
                if total1.startswith(val) and total2.startswith(val):
                    streak += 1
                else: 
                    break
            else:
                return False
        return streak
    async def max_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_streak = 0
        max_streak = 0

        async for game in all_games():
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val) and \
                game[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    # max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy9(last_games, all_games, all_games_rev):
    val = 'TM'
    round1_num, round2_num = 2, 3
    games_reversed = last_games
    last_game = games_reversed[0]['game_id']
    async def cur_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game[total1_key_name]
            total2 = game[total2_key_name]
            if total1 and total2:
                if total1.startswith(val) and total2.startswith(val):
                    streak += 1
                else: 
                    break
            else:
                return False
        return streak
    async def max_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_streak = 0
        max_streak = 0

        async for game in all_games():
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val) and \
                game[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    # max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy10(last_games, all_games, all_games_rev):
    val1 = 'TB'
    val2 = 'TM'
    round1_num, round2_num = 1, 2
    games_reversed = last_games
    last_game = games_reversed[0]['game_id']
    async def cur_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game[total1_key_name]
            total2 = game[total2_key_name]
            if total1 and total2:
                if total1.startswith(val1) and total2.startswith(val2):
                    streak += 1
                else: 
                    break
            else:
                return False
        return streak
    async def max_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_streak = 0
        max_streak = 0

        async for game in all_games():
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val1) and \
                game[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    # max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy11(last_games, all_games, all_games_rev):
    val1 = 'TB'
    val2 = 'TM'
    round1_num, round2_num = 2, 3
    games_reversed = last_games
    last_game = games_reversed[0]['game_id']
    async def cur_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game[total1_key_name]
            total2 = game[total2_key_name]
            if total1 and total2:
                if total1.startswith(val1) and total2.startswith(val2):
                    streak += 1
                else: 
                    break
            else:
                return False
        return streak
    async def max_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_streak = 0
        max_streak = 0

        async for game in all_games():
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val1) and \
                game[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    # max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy12(last_games, all_games, all_games_rev):
    val1 = 'TM'
    val2 = 'TB'
    round1_num, round2_num = 1, 2
    games_reversed = last_games
    last_game = games_reversed[0]['game_id']
    async def cur_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game[total1_key_name]
            total2 = game[total2_key_name]
            if total1 and total2:
                if total1.startswith(val1) and total2.startswith(val2):
                    streak += 1
                else: 
                    break
            else:
                return False
        return streak
    async def max_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_streak = 0
        max_streak = 0

        async for game in all_games():
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val1) and \
                game[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    # max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy13(last_games, all_games, all_games_rev):
    val1 = 'TM'
    val2 = 'TB'
    round1_num, round2_num = 2, 3
    games_reversed = last_games
    last_game = games_reversed[0]['game_id']
    async def cur_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game[total1_key_name]
            total2 = game[total2_key_name]
            if total1 and total2:
                if total1.startswith(val1) and total2.startswith(val2):
                    streak += 1
                else: 
                    break
            else:
                return False
        return streak
    async def max_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_streak = 0
        max_streak = 0

        async for game in all_games():
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val1) and \
                game[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    # max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'
'''


async def test():
    import db
    print('test')
    games = db.get_many_games('all')
    from named_tuples import get_total_streak_count
    a = await ochka_stat(games, 5)
    data = {}
    for players, totals in a.items():
        for total, subtotals in totals.items():
            if total not in data.keys():
                data[total] = {}
            for subtotal, value in subtotals.items():
                if not subtotal in data[total].keys():
                    data[total][subtotal] = 0
                data[total][subtotal] += value
    print('######################################################')
    print(data)


if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
