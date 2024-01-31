import db
import asyncio


def main():
    loop = asyncio.get_event_loop()
    games = loop.run_until_complete(db.get_games())
    res = games.round_total_last_streak(round_num=1)
    print(res)

if __name__=='__main__':
    main()