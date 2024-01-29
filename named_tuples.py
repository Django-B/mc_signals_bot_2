from typing import NamedTuple
import datetime


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

