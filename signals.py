import db
import asyncio


class Strategy:

    def __init__ (self, games):
        self.games = games

    def round_total_max_streak(self, round_num: int):
        '''Возвращает максимальные длины серий тоталов(TB, TM) в нужном раунде всех игр'''
        pass

    def round_total_last_streak(self, round_num: int) -> tuple[str, int]:
        '''Возвращает длину последней серии тоталов(TB, TM) в нужном раунде последних игр'''
        games_reversed = self.games[::-1]  # игры от новых к старым 
        total_key = f'round{round_num}_total'
        last_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total = game._asdict()[total_key]
            if total and not flag:
                last_total = total[0:2]
                streak += 1
                flag = True
            elif total and flag:
                if total[0:2]==last_total:
                    streak += 1
                else: 
                    break
        return last_total, streak
        


        

def main():
    loop = asyncio.get_event_loop()
    games = loop.run_until_complete(db.get_games())
    strategy = Strategy(games)
    res = strategy.round_total_last_streak(1)
    print(res)

if __name__=='__main__':
    main()