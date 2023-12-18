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
) -> tuple[datetime.date, datetime.time] | None:
    regex = r'(?P<time>\d\d:\d\d) (?P<date>\d\d-\d\d-\d\d\d\d)'
    res = re.search(regex, message_text)
    if not res: return None
    str_time, str_date = res.groups()
    time = datetime.datetime.strptime(str_time, "%H:%M").time()
    date = datetime.datetime.strptime(str_date, "%d-%m-%Y").date()

    return date, time

async def extract_pnames(message_text: str) -> tuple[str, str] | None:
    regex = '#(?P<p1>[А-Яа-я]+) #(?P<p2>[А-Яа-я]+)'
    res = re.search(regex, message_text)
    if not res: return None
    return res.groups() 

async def extract_p_game_win_coefs(message_text: str) -> tuple[float, float] | None:
    regex = r' {2,4}[A-z]\d[A-z]\|[A-z]\d[A-z] . (?P<p1_win_coef>\d+\.\d+)\|(?P<p2_win_coef>\d+\.\d+)'
    res = re.search(regex, message_text)
    if not res: return None
    p1_coef, p2_coef = map(float, res.groups())
    return p1_coef, p2_coef

async def extract_p_round_win_coefs(message_text: str) -> tuple[float, float] | None:
    regex = r'[A-z]\d\/[A-z]\d +. +(?P<p1_coef>\d+\.\d+)\/(?P<p2_coef>\d+\.\d+)'
    res = re.search(regex, message_text)
    if not res: return None
    p1_coef, p2_coef = map(float, res.groups())
    return p1_coef, p2_coef

async def extract_fbr(message_text: str) -> tuple[float, float, float] | None:
    regex = r'[f|F][b|B][r|R] +. +(?P<f>\d+\.\d+) +\| +(?P<b>\d+\.\d+) +\| +(?P<r>\d+\.\d+)'
    res = re.search(regex, message_text)
    if not res: return None
    f, b, r = map(float, res.groups())
    return f, b, r

async def extract_nums_totals(
    message_text: str
) -> tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float]
] | None:
    '''
    Returns tuple: (
        (min_num_total, min_num_total_min_coef, min_num_total_max_coef),
        (mid_num_total, mid_num_total_min_coef, mid_num_total_max_coef),
        (max_num_total, max_num_total_min_coef, max_num_total_max_coef)
    )
    '''
    regex = r'(?P<total>\d+\.\d+) +\((?P<min_coef>\d+\.\d+) +. +(?P<max_coef>\d+\.\d+)\)'
    res = re.findall(regex, message_text)
    if not res: return None
    return tuple(map(lambda x: tuple([float(i) for i in x]), res))

async def extract_f(message_text: str) -> tuple[float, float] | None:
    '''Returns FYes, FNo coefs'''
    regex = r'FYes +. *(?P<fyes>[\d\.]+) +FNo +. *(?P<fno>[\d\.]+)'
    res = re.search(regex, message_text)
    if not res: return None
    return tuple(map(float, res.groups()))

async def extract_p_wins(message_text: str) -> tuple[int, int] | None:
    '''Returns p1_wins, p2_wins'''
    regex = r'(?P<p1_wins>\d+):(?P<p2_wins>\d+)\n'
    res = re.search(regex, message_text)
    if not res: return None
    return tuple(map(int, res.groups()))

async def extract_round_total(message_text: str, round_num: int) -> str | None:
    '''Возвращает тотал нужного раунда игры(TB, TBB, TM, TMM)'''
    if not message_text:
        return None

    regex = r"{}. +[A-Z][0-9].+[A-Z].+\d\s+(?P<total>[A-Z]+)".format(str(round_num))
    res = re.search(regex, message_text)
    if res:
        return res.group('total')
    return None

async def extract_game_data(message) -> Game: # type: ignore
    message_id = message.id

async def main():
    a = await extract_p_wins(test_message)
    pprint(a)
    

if __name__=='__main__':
    asyncio.run(main())
