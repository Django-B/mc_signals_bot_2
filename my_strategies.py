from named_tuples import Games
import asyncio


strategies = []

def strategy(func):
    strategies.append(func)
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
    return wrapper


@strategy
async def strategy1(games: Games):
    '''Текущая серия ТБ и ТМ 1-го раунда = 10'''
    round_num = 1
    cur_streak = await games.cur_round_total_streak(round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    print(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}'

@strategy
async def strategy2(games: Games):
    '''Текущая серия ТБ и ТМ 2-го раунда = 10'''
    round_num = 2
    cur_streak = await games.cur_round_total_streak(round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    print(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}'

@strategy
async def strategy3(games: Games):
    '''Текущая серия ТБ и ТМ 3-го раунда = 10'''
    round_num = 3
    cur_streak = await games.cur_round_total_streak(round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    print(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}'

@strategy
async def strategy4(games: Games):
    '''Текущая серия ТБ и ТМ 4-го раунда = 10'''
    round_num = 4
    cur_streak = await games.cur_round_total_streak(round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    print(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}'

@strategy
async def strategy5(games: Games):
    '''Текущая серия ТБ и ТМ 5-го раунда = 10'''
    round_num = 5
    cur_streak = await games.cur_round_total_streak(round_num=round_num)
    #max_streak = await games.max_round_total_streak(total_name=cur_streak.total, round_num=round_num)
    print(f'Текущая серия { cur_streak.total } { round_num }-го раунда = {cur_streak.streak}')
    if cur_streak.streak >= 10:
        return f'Серия {cur_streak.total } в {round_num}-м раунде достигла {cur_streak.streak}'

@strategy
async def strategy6(games: Games):
    '''Текущая серия игр ТБ в 1-м и 2-м раундах >= 10'''
    val = 'TB'
    round1_num, round2_num = 1, 2
    async def cur_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        games_reversed = games[::-1]  # игры от новых к старым 
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game._asdict()[total1_key_name]
            total2 = game._asdict()[total2_key_name]
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

        for game in games:
            if game._asdict()[total1_key_name] and game._asdict()[total2_key_name] and \
                game._asdict()[total1_key_name].startswith(val) and \
                game._asdict()[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}'

@strategy
async def strategy7(games: Games):
    '''Текущая серия игр ТБ в 2-м и 3-м раундах >= 10'''
    val = 'TB'
    round1_num, round2_num = 2, 3
    async def cur_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        games_reversed = games[::-1]  # игры от новых к старым 
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game._asdict()[total1_key_name]
            total2 = game._asdict()[total2_key_name]
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

        for game in games:
            if game._asdict()[total1_key_name] and game._asdict()[total2_key_name] and \
                game._asdict()[total1_key_name].startswith(val) and \
                game._asdict()[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}'

@strategy
async def strategy8(games: Games):
    '''Текущая серия игр ТM в 1-м и 2-м раундах >= 10'''
    val = 'TM'
    round1_num, round2_num = 1, 2
    async def cur_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        games_reversed = games[::-1]  # игры от новых к старым 
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game._asdict()[total1_key_name]
            total2 = game._asdict()[total2_key_name]
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

        for game in games:
            if game._asdict()[total1_key_name] and game._asdict()[total2_key_name] and \
                game._asdict()[total1_key_name].startswith(val) and \
                game._asdict()[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}'

@strategy
async def strategy9(games: Games):
    '''Текущая серия игр ТM в 2-м и 3-м раундах >= 10'''
    val = 'TM'
    round1_num, round2_num = 2, 3
    async def cur_streak(val: str = val, round1_num: int = round1_num, round2_num: int = round2_num):
        games_reversed = games[::-1]  # игры от новых к старым 
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game._asdict()[total1_key_name]
            total2 = game._asdict()[total2_key_name]
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

        for game in games:
            if game._asdict()[total1_key_name] and game._asdict()[total2_key_name] and \
                game._asdict()[total1_key_name].startswith(val) and \
                game._asdict()[total2_key_name].startswith(val):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}'

@strategy
async def strategy10(games: Games):
    '''Текущая серия игр TB+ТM в 1-м и 2-м раундах >= 10'''
    val1 = 'TB'
    val2 = 'TM'
    round1_num, round2_num = 1, 2
    async def cur_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        games_reversed = games[::-1]  # игры от новых к старым 
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game._asdict()[total1_key_name]
            total2 = game._asdict()[total2_key_name]
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

        for game in games:
            if game._asdict()[total1_key_name] and game._asdict()[total2_key_name] and \
                game._asdict()[total1_key_name].startswith(val1) and \
                game._asdict()[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}'

@strategy
async def strategy11(games: Games):
    '''Текущая серия игр TB+ТM в 2-м и 3-м раундах >= 10'''
    val1 = 'TB'
    val2 = 'TM'
    round1_num, round2_num = 2, 3
    async def cur_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        games_reversed = games[::-1]  # игры от новых к старым 
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game._asdict()[total1_key_name]
            total2 = game._asdict()[total2_key_name]
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

        for game in games:
            if game._asdict()[total1_key_name] and game._asdict()[total2_key_name] and \
                game._asdict()[total1_key_name].startswith(val1) and \
                game._asdict()[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}'

@strategy
async def strategy12(games: Games):
    '''Текущая серия игр ТM+TB в 1-м и 2-м раундах >= 10'''
    val1 = 'TM'
    val2 = 'TB'
    round1_num, round2_num = 1, 2
    async def cur_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        games_reversed = games[::-1]  # игры от новых к старым 
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game._asdict()[total1_key_name]
            total2 = game._asdict()[total2_key_name]
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

        for game in games:
            if game._asdict()[total1_key_name] and game._asdict()[total2_key_name] and \
                game._asdict()[total1_key_name].startswith(val1) and \
                game._asdict()[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}'

@strategy
async def strategy13(games: Games):
    '''Текущая серия игр ТM+TB в 2-м и 3-м раундах >= 10'''
    val1 = 'TM'
    val2 = 'TB'
    round1_num, round2_num = 2, 3
    async def cur_streak(val1: str = val1, val2: str = val2, round1_num: int = round1_num, round2_num: int = round2_num):
        games_reversed = games[::-1]  # игры от новых к старым 
        total1_key_name = f'round{round1_num}_total'
        total2_key_name = f'round{round2_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total1 = game._asdict()[total1_key_name]
            total2 = game._asdict()[total2_key_name]
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

        for game in games:
            if game._asdict()[total1_key_name] and game._asdict()[total2_key_name] and \
                game._asdict()[total1_key_name].startswith(val1) and \
                game._asdict()[total2_key_name].startswith(val2):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    cur_streak = await cur_streak()
    max_streak = await max_streak()
    if cur_streak >= 10:
        return f'Текущая серия игр {val1} и {val2} в {round1_num}-м и {round2_num}-м раундах = {cur_streak}'



async def test():
    await dump_channel_history()
    games = await db.get_games()
    res = await strategy1(games)
    print(res)

if __name__=='__main__':
    from history import dump_channel_history
    import db
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())