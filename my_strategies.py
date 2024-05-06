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


streak_limit = 2

@strategy
async def strategytb(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 1-го раунда = 10'''
    games = last_games

    total = 'TB'

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
        if cur_streak.streak >= streak_limit:
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= streak_limit and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals

@strategy
async def strategytbb(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 1-го раунда = 10'''
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
        if cur_streak.streak >= streak_limit:
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= streak_limit and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals


@strategy
async def strategytbbb(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 1-го раунда = 10'''
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
        if cur_streak.streak >= streak_limit:
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= streak_limit and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals

@strategy
async def strategytm(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 1-го раунда = 10'''
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
        if cur_streak.streak >= streak_limit:
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= streak_limit and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals

@strategy
async def strategytmm(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 1-го раунда = 10'''
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
        if cur_streak.streak >= streak_limit:
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= streak_limit and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals


@strategy
async def strategytmmm(last_games, all_games, all_games_rev):
    '''Текущая серия ТБ и ТМ 1-го раунда = 10'''
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
        if cur_streak.streak >= streak_limit:
            signals.append(f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}❌\nhttps://t.me/statamk10/{last_game}')

        elif cur_streak2.streak >= streak_limit and real_cur_streak.streak == 1:
            signals.append(f'Серия {cur_streak2.total } из {cur_streak2.streak} в {round_num}-м раунде прервалась✅\nhttps://t.me/statamk10/{last_game}')
    return signals



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


async def test():
    import db
    print('test')
    games = db.get_many_games('all')
    from named_tuples import get_total_streak_count
    a = await get_total_streak_count(lambda: games, 'TB', 1)
    print(a)

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
