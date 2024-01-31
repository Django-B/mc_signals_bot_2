from named_tuples import Games


strategies = []

def strategy(func):
    strategies.append(func)
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
    return wrapper

@strategy
async def strategy1(games: Games, round_num: int = 1 ) -> bool:
    last_total_streak = await games.round_total_last_streak(round_num=round_num)
    max_total_streak = await games.round_total_max_streak(last_total_streak[0], round_num=round_num)
    if last_total_streak in (max_total_streak[1], max_total_streak[1]-1, max_total_streak[1]-2):
        return f'Текущая серия тоталов {round_num} раунда достигла максимального значения'\
            'Текущая: {last_total_streak[1]}, Макс.: {max_total_streak[1]}'
    return False
    
@strategy
async def strategy2(games: Games, round_num: int = 1 ) -> bool:
    cleaned_games = [x for x in games if x.round1_total]
    cur_total = cleaned_games[-1].round1_total[0:2]
    return f'Тотал первого раунда последнего боя: {cur_total}\n'\
        f'Ставь на {cur_total} в следующем бою'
