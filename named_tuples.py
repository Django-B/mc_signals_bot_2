from typing import NamedTuple
from collections import UserList
import datetime


class DotDict(dict):
    """Класс, представляющий собой словарь, к элементам которого можно обращаться через точку."""
    def __init__(self, d: dict):
        self.d = d

    def get_value(self):
        return self.d

    def __getattr__(self, item: str) -> 'WrapperMap':
        return self.d.get(item)

    def __repr__(self):
        return repr(self.d)

class Strategies(UserList):
    async def get_signals(self, games):
        pass

class Games(UserList):
    async def max_round_total_streak(self, total_name: str, round_num: int = 1):
        '''Возвращает максимальные длины серий тоталов(TB, TM) в нужном раунде всех игр'''
        total_name = total_name[0:2]
        total_key_name = f'round{round_num}_total'
        cur_streak = 0
        max_streak = 0
        
        for game in self.data:
            if game._asdict()[total_key_name] and game._asdict()[total_key_name].startswith(total_name):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return DotDict({'total': total_name, 'streak': max_streak})

    async def cur_round_total_streak(self, round_num: int = 1) -> tuple[str, int]:
        '''Возвращает длину последней серии тоталов(TB, TM) в нужном раунде последних игр'''
        games_reversed = self.data[::-1]  # игры от новых к старым 
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
        return DotDict({'total': cur_total, 'streak': streak})

    async def get_max_streak(self, field_name: str, right_value):
        '''Возвращает максимальную длину серии field_name(нужного исхода) cо значением right_value'''
        cur_streak = 0
        max_streak = 0
        
        for game in self.data:
            if game._asdict()[field_name] and str(game._asdict()[field_name]) == str(right_value):
                cur_streak += 1
            else:
                max_streak = max(max_streak, cur_streak)
                cur_streak = 0
        return max_streak

    async def get_cur_streak(self, field_name: str):
        '''Возвращает длину последней серии field_name(нужного исхода)'''
        games_reversed = self.data[::-1]  # игры от новых к старым 
        cur_total = None
        streak = 0
        flag = False
        for game in games_reversed:
            total = game._asdict()[field_name]
            if total:
                if not flag:
                    cur_total = total
                    streak += 1
                    flag = True
                elif flag:
                    if total==cur_total:
                        streak += 1
                    else: 
                        break
        return DotDict({'total': cur_total, 'streak': streak})

class Game(NamedTuple):
    game_id: int

    game_date: datetime.date
    game_time: datetime.time

    p1_name: str
    p2_name: str

    p1_game_win_coef: float
    p2_game_win_coef: float

    p1_round_win_coef: float
    p2_round_win_coef: float

    f_coef: float
    b_coef: float
    r_coef: float

    min_num_total: float
    min_num_total_min_coef: float
    min_num_total_max_coef: float
    
    mid_num_total: float
    mid_num_total_min_coef: float
    mid_num_total_max_coef: float

    max_num_total: float
    max_num_total_min_coef: float
    max_num_total_max_coef: float

    fyes: float
    fno: float

    p1_wins: int
    p2_wins: int

    round1_winner: str | None
    round1_finish: str | None
    round1_time: str | None
    round1_total: str | None

    round2_winner: str | None
    round2_finish: str | None
    round2_time: str | None
    round2_total: str | None

    round3_winner: str | None
    round3_finish: str | None
    round3_time: str | None
    round3_total: str | None

    round4_winner: str | None
    round4_finish: str | None
    round4_time: str | None
    round4_total: str | None

    round5_winner: str | None
    round5_finish: str | None
    round5_time: str | None
    round5_total: str | None

    round6_winner: str | None
    round6_finish: str | None
    round6_time: str | None
    round6_total: str | None

    round7_winner: str | None
    round7_finish: str | None
    round7_time: str | None
    round7_total: str | None

    round8_winner: str | None
    round8_finish: str | None
    round8_time: str | None
    round8_total: str | None

    round9_winner: str | None
    round9_finish: str | None
    round9_time: str | None
    round9_total: str | None

