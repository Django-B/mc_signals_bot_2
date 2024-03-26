import asyncio

from logger import logger
from named_tuples import Games
from named_tuples import cur_round_total_streak, max_round_total_streak, get_max_streak, get_cur_streak


strategies = []

def strategy(func):
    strategies.append(func)
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
    return wrapper


@strategy
async def strategy1(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 1-го раунда = 10'''
    round_num = 1
    games = last_games
    last_game = games[0]['game_id']
    cur_streak = await cur_round_total_streak(games, round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy2(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 2-го раунда = 10'''
    round_num = 2
    games = last_games
    last_game = games[0]['game_id']
    cur_streak = await cur_round_total_streak(games, round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy3(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 3-го раунда = 10'''
    round_num = 3
    games = last_games
    last_game = games[0]['game_id']
    cur_streak = await cur_round_total_streak(games, round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy4(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 4-го раунда = 10'''
    round_num = 4
    games = last_games
    last_game = games[0]['game_id']
    cur_streak = await cur_round_total_streak(games, round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy5(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 5-го раунда = 10'''
    round_num = 5
    games = last_games
    last_game = games[0]['game_id']
    cur_streak = await cur_round_total_streak(games, round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    logger.info(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy6(last_games, all_games, all_games_rev):
    '''Текущая серия игр ТБ в 1-м и 2-м раундах >= 10'''
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

        async for game in all_games:
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val) and \
                game[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy7(last_games, all_games, all_games_rev):
    '''Текущая серия игр ТБ в 2-м и 3-м раундах >= 10'''
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

        async for game in all_games:
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val) and \
                game[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy8(last_games, all_games, all_games_rev):
    '''Текущая серия игр ТM в 1-м и 2-м раундах >= 10'''
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

        async for game in all_games:
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val) and \
                game[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy9(last_games, all_games, all_games_rev):
    '''Текущая серия игр ТM в 2-м и 3-м раундах >= 10'''
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

        async for game in all_games:
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val) and \
                game[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy10(last_games, all_games, all_games_rev):
    '''Текущая серия игр TB+ТM в 1-м и 2-м раундах >= 10'''
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

        async for game in all_games:
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val1) and \
                game[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy11(last_games, all_games, all_games_rev):
    '''Текущая серия игр TB+ТM в 2-м и 3-м раундах >= 10'''
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
                if total1.startswith(val) and total2.startswith(val2):
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

        async for game in all_games:
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val1) and \
                game[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy12(last_games, all_games, all_games_rev):
    '''Текущая серия игр ТM+TB в 1-м и 2-м раундах >= 10'''
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
                if total1.startswith(val) and total2.startswith(val2):
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

        async for game in all_games:
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val1) and \
                game[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'

@strategy
async def strategy13(last_games, all_games, all_games_rev):
    '''Текущая серия игр ТM+TB в 2-м и 3-м раундах >= 10'''
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
                if total1.startswith(val) and total2.startswith(val2):
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

        async for game in all_games:
            if game[total1_key_name] and game[total2_key_name] and \
                game[total1_key_name].startswith(val1) and \
                game[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}\nhttps://t.me/statamk10/{last_game}'


async def test_strategy():
    res = await cur_round_total_streak(games, 4)
    print(res)


async def test():
    #await dump_channel_history()
    games = await db.get_games()
    res = await test_strategy(games)
    print(res)

if __name__=='__main__':
    from history import dump_channel_history
    import db
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())