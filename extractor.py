import re
import asyncio
import datetime

from named_tuples import Game
from pprint import pprint


test_message = '''18:45 18-12-2023 #N1186 #L2
#ТреморДиВора
#Тремор #ДиВора
   P1m|P2m - 1.15|5.43
P1/P2 - 1.48/2.73
FBR - 4.23 | 6.28 | 1.43
#t7v8     atv : 32.83
TimeStat(Больше-Меньше:O-U)
25.5 (1.22 - 4.18)   #m25
32.5 (1.88 - 2.025)   #s32
40.5 (3.86 - 1.25)   #b40
FYes -4.23    FNo -1.22

5:2
1. P1--R--29  TM
2. P2--F--32  TM
3. P1--R--53  TBB
4. P1--R--30  TM
5. P2--R--33  TB
6. P1--B--43  TBB
7. P1--R--41  TBB 
   #T7'''

async def extract_date_and_time(
    message_text: str
) -> tuple[datetime.date, datetime.time] | tuple[None, None]:
    regex1 = r'(?P<time>\d\d:\d\d) (?P<date>\d\d-\d\d-\d\d\d\d)'
    regex2 = r'(?P<time>\d\d:\d\d) (?P<date>\d\d\d\d-\d\d-\d\d)'
    res1 = re.search(regex1, message_text)
    res2 = re.search(regex2, message_text)
    res = res1
    if not res1:
        if not res2:
            return None, None
        else:
            res = res2
    str_time, str_date = res.groups()
    time = datetime.datetime.strptime(str_time, "%H:%M").time()
    date = datetime.datetime.strptime(str_date, "%Y-%m-%d").date()

    return date, time

async def extract_p_names(message_text: str) -> tuple[str, str] | tuple[None, None]:
    regex = '#(?P<p1>[А-Яа-я]+).*#(?P<p2>[А-Яа-я]+)'
    res = re.search(regex, message_text)
    if not res: return None, None
    return res.groups() 

async def extract_p_game_win_coefs(message_text: str) -> tuple[float, float] | tuple[None, None]:
    regex = r' {2,4}[A-z]\d[A-z]\|[A-z]\d[A-z] . (?P<p1_win_coef>\d+\.\d+)\|(?P<p2_win_coef>\d+\.\d+)'
    res = re.search(regex, message_text)
    if not res: return None, None
    p1_coef, p2_coef = map(float, res.groups())
    return p1_coef, p2_coef

async def extract_p_round_win_coefs(message_text: str) -> tuple[float, float] | tuple[None, None]:
    regex = r'[A-z]\d\/[A-z]\d +. +(?P<p1_coef>\d+\.\d+)\/(?P<p2_coef>\d+\.\d+)'
    res = re.search(regex, message_text)
    if not res: return None, None
    p1_coef, p2_coef = map(float, res.groups())
    return p1_coef, p2_coef

async def extract_fbr(message_text: str) -> tuple[float, float, float] | tuple[None, None, None]:
    regex = r'[f|F][b|B][r|R] +. +(?P<f>\d+\.\d+) +\| +(?P<b>\d+\.\d+) +\| +(?P<r>\d+\.\d+)'
    res = re.search(regex, message_text)
    if not res: return None, None, None
    f, b, r = map(float, res.groups())
    return f, b, r

async def extract_nums_totals(
    message_text: str
) -> tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float]
] | tuple[None, None, None]:
    '''
    Returns tuple: (
        (min_num_total, min_num_total_min_coef, min_num_total_max_coef),
        (mid_num_total, mid_num_total_min_coef, mid_num_total_max_coef),
        (max_num_total, max_num_total_min_coef, max_num_total_max_coef)
    )
    '''
    # regex = r'(?P<total>\d+\.\d+) +\((?P<min_coef>\d+\.\d+) +. +(?P<max_coef>\d+\.\d+)\)'
    regex = r'/(?P<total>\d+(\.\d+)*) +\((?P<min_coef>\d+(\.\d+)*) +. +(?P<max_coef>\d+(\.\d+)*)\)'
    res = re.findall(regex, message_text)
    if not res: return [[None for x in range(3)], [None for x in range(3)], [None for x in range(3)], ]
    return tuple(map(lambda x: tuple([float(i) for i in x]), res))

async def extract_f(message_text: str) -> tuple[float, float] | tuple[None, None]:
    '''Returns FYes, FNo coefs'''
    regex = r'FYes +. *(?P<fyes>[\d\.]+) +FNo +. *(?P<fno>[\d\.]+)'
    res = re.search(regex, message_text)
    if not res: return None, None
    return tuple(map(float, res.groups()))

async def extract_p_wins(message_text: str) -> tuple[int, int] | tuple[None, None]:
    '''Returns p1_wins, p2_wins'''
    regex = r'(?P<p1_wins>\d+):(?P<p2_wins>\d+)\n'
    res = re.search(regex, message_text)
    if not res: return None, None
    return tuple(map(int, res.groups()))

async def extract_round_data(message_text: str, round_num: int) -> dict:
    regex = r'{}\. +(?P<winner>[A-z\d]+).+(?P<finish>[A-z]+).+(?P<time>[\d]+) +(?P<total>[A-z]+)'.format(round_num)
    res = re.search(regex, message_text)
    if not res:
        return {'winner':None, 'finish':None,'time':None, 'total':None}
    data = {
        'winner': res.group('winner'),
        'finish': res.group('finish'),
        'time': int(res.group('time')),
        'total': res.group('total')
    }
    return data

async def extract_game_data(message) -> Game | None: # type: ignore
    message_id = message.id
    message_text = message.raw_text
    date, time = await extract_date_and_time(message_text)
    p1, p2 = await extract_p_names(message_text)
    p1_game_win_coef, p2_game_win_coef  = await extract_p_game_win_coefs(message_text)
    p1_round_win_coef, p2_round_win_coef  = await extract_p_round_win_coefs(message_text)
    f, b, r = await extract_fbr(message_text)
    min_num_totals, mid_num_totals, max_num_totals = await extract_nums_totals(message_text)
    fyes, fno = await extract_f(message_text)
    p1_wins, p2_wins = await extract_p_wins(message_text)
    round1 = await extract_round_data(message_text, 1)
    round2 = await extract_round_data(message_text, 2)
    round3 = await extract_round_data(message_text, 3)
    round4 = await extract_round_data(message_text, 4)
    round5 = await extract_round_data(message_text, 5)
    round6 = await extract_round_data(message_text, 6)
    round7 = await extract_round_data(message_text, 7)
    round8 = await extract_round_data(message_text, 8)
    round9 = await extract_round_data(message_text, 9)
    
    if not all([
        date,
        time,
        p1,
        p2,
        round1.values()
    ]):
        return None

    game = Game(
        message_id=message_id,
        game_date=date, # type: ignore
        game_time=time, # type: ignore
        p1_name=p1, # type: ignore
        p2_name=p2, # type: ignore
        p1_game_win_coef=p1_game_win_coef, # type: ignore
        p2_game_win_coef=p2_game_win_coef, # type: ignore
        p1_round_win_coef=p1_round_win_coef, # type: ignore
        p2_round_win_coef=p2_round_win_coef, # type: ignore
        f_coef=f, # type: ignore
        b_coef=b, # type: ignore
        r_coef=r, # type: ignore
        min_num_total=min_num_totals[0], # type: ignore
        min_num_total_min_coef=min_num_totals[1], # type: ignore
        min_num_total_max_coef=min_num_totals[2], # type: ignore
        mid_num_total=mid_num_totals[0], # type: ignore
        mid_num_total_min_coef=mid_num_totals[1], # type: ignore
        mid_num_total_max_coef=mid_num_totals[2], # type: ignore
        max_num_total=max_num_totals[0], # type: ignore
        max_num_total_min_coef=max_num_totals[1], # type: ignore
        max_num_total_max_coef=max_num_totals[2], # type: ignore
        fyes=fyes, # type: ignore
        fno=fno, # type: ignore
        p1_wins=p1_wins, # type: ignore
        p2_wins=p2_wins, # type: ignore
        round1_winner=round1['winner'], # type: ignore
        round1_finish=round1['finish'], # type: ignore
        round1_time=round1['time'], # type: ignore
        round1_total=round1['total'], # type: ignore
        round2_winner=round2['winner'], # type: ignore
        round2_finish=round2['finish'], # type: ignore
        round2_time=round2['time'], # type: ignore
        round2_total=round2['total'], # type: ignore
        round3_winner=round3['winner'], # type: ignore
        round3_finish=round3['finish'], # type: ignore
        round3_time=round3['time'], # type: ignore
        round3_total=round3['total'], # type: ignore
        round4_winner=round4['winner'], # type: ignore
        round4_finish=round4['finish'], # type: ignore
        round4_time=round4['time'], # type: ignore
        round4_total=round4['total'], # type: ignore
        round5_winner=round5['winner'], # type: ignore
        round5_finish=round5['finish'], # type: ignore
        round5_time=round5['time'], # type: ignore
        round5_total=round5['total'], # type: ignore
        round6_winner=round6['winner'], # type: ignore
        round6_finish=round6['finish'], # type: ignore
        round6_time=round6['time'], # type: ignore
        round6_total=round6['total'], # type: ignore
        round7_winner=round7['winner'], # type: ignore
        round7_finish=round7['finish'], # type: ignore
        round7_time=round7['time'], # type: ignore
        round7_total=round7['total'], # type: ignore
        round8_winner=round8['winner'],
        round8_finish=round8['finish'], # type: ignore
        round8_time=round8['time'], # type: ignore
        round8_total=round8['total'], # type: ignore
        round9_winner=round9['winner'], # type: ignore
        round9_finish=round9['finish'], # type: ignore
        round9_time=round9['time'], # type: ignore
        round9_total=round9['total'] # type: ignore
    )

    return game


async def main():
    a = await extract_game_data(test_message)
    pprint(a)
    

if __name__=='__main__':
    asyncio.run(main())
