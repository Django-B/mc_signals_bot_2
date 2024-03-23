import db
import asyncio
from my_strategies import strategies


async def check_all_signals():
    '''Проверяет есть ли совпадения по стратегиям и возвращает их ответы'''
    signals = []
    for signal in strategies:
        res = await signal()
        if res:
            signals.append(res)
    return signals



async def main():
    print(strategies)

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
