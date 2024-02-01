from named_tuples import Games
import asyncio


strategies = []

def strategy(func):
    strategies.append(func)
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
    return wrapper

@strategy
async def strategy1(games: Games): # комментарий
    '''комментарий'''
    last_total_streak = await games.cur_round_total_streak()
    max_total_streak = await games.max_round_total_streak(last_total_streak.total)
    if last_total_streak.streak in (max_total_streak.streak, max_total_streak.streak-1, max_total_streak.streak-2):
        return f'Текущая серия тоталов {round_num} раунда достигла максимального значения\n'\
            'Текущая: {last_total_streak.streak}, Макс.: {max_total_streak.streak}'
    else:
        return False

# @strategy
# async def strategy2(games: Games):
#     cleaned_games = [x for x in games if x.round1_total]
#     cur_total = cleaned_games[-1].round1_total[0:2]
#     return f'Тотал первого раунда последнего боя: {cur_total}\nСтавь на {cur_total} в следующем бою'

async def main():
    pass

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())