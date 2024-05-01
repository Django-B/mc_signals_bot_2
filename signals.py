import db
import asyncio
from my_strategies import strategies
from db import get_some_games, get_many_games

async def check_all_signals():
    '''Проверяет есть ли совпадения по стратегиям и возвращает их ответы'''
    signals=[]
    last_games = await get_some_games(-200)
    all_games = lambda: get_many_games('all')
    all_games_rev = lambda: get_many_games('-all')
    # wrap_strategies = [strategy(last_games, all_games, all_games_rev) for strategy in strategies]
    for signal in strategies:
        res = await signal(last_games, all_games, all_games_rev)
        if res:
            if type(res)==list:
                signals.extend(res)
            else:
                signals.append(res)
    # signals = await asyncio.gather(*wrap_strategies)
    return [signal for signal in signals if signal]



async def main():
    print(strategies)

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
