import db
import asyncio


class Strategy:

    def __init__ (self, games):
        self.games = games

    def round_total_max_streak(self, total_name: str, round_num: int):
        '''Возвращает максимальные длины серий тоталов(TB, TM) в нужном раунде всех игр'''
        total_key_name = f'round{round_num}_total'
        cur_streak = 0
        max_streak = 0
        
        for game in self.games:
            if game._asdict()[total_key_name] and game._asdict()[total_key_name].startswith(total_name):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return total_name, max_streak

    def round_total_last_streak(self, round_num: int) -> tuple[str, int]:
        '''Возвращает длину последней серии тоталов(TB, TM) в нужном раунде последних игр'''
        games_reversed = self.games[::-1]  # игры от новых к старым 
        total_key_name = f'round{round_num}_total'
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total = game._asdict()[total_key_name]
            if total:
                if not flag:
                    cur_total = total[0:2]
                    streak += 1
                    flag = True
                elif flag:
                    if total[0:2]==cur_total:
                        streak += 1
                    else: 
                        break
        return cur_total, streak
        

def main():
    loop = asyncio.get_event_loop()
    games = loop.run_until_complete(db.get_games())
    strategy = Strategy(games)
    res = strategy.round_total_last_streak(1)
    res = strategy.round_total_max_streak('TB', 1)
    print(res)
    res = strategy.round_total_max_streak('TM', 1)
    print(res)

if __name__=='__main__':
    main()