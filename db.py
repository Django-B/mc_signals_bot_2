from collections.abc import AsyncGenerator
import aiosqlite, asyncio
from logger import logger
from enum import Enum
from typing import Iterable

from get_config import get_config
from named_tuples import Game
from decorators import *

config = get_config()

DB_NAME = str(config['db_name'])
# CHANNEL_NAME = config['target_channel_url'].split('/')[-1]
USERS_TABLE_NAME = 'bot_user'
GAME_TABLE_NAME = 'game'



class QueryType(Enum):
    COMMIT = 'commit'
    FETCH = 'fetch'

@retry_on_locked_database()
async def execute(query: str, query_type: QueryType) -> Iterable[aiosqlite.Row] | AsyncGenerator[aiosqlite.Row] |  None:
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.cursor()
        await cursor.execute(query)
        if query_type == QueryType.COMMIT:
            await db.commit()
        elif query_type == QueryType.FETCH:
            return await cursor.fetchall() # type: ignore


async def commit(query) -> None:
    await execute(query, QueryType.COMMIT)


async def fetch(query) -> Iterable[aiosqlite.Row]:
    return await execute(query, QueryType.FETCH) # type: ignore

@retry_on_locked_database_yield()
async def fetchmany(query):
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.cursor()
        await cursor.execute(query)
        while True:
            rows = await cursor.fetchmany(20)
            if not rows:
                break
            for row in rows:
                yield row


async def create_tables():
    with open('game.sql') as f:
        game_table_query = f.read()
    with open('owner.sql') as f:
        owner_table_query = f.read()

    await commit(game_table_query)
    await commit(owner_table_query)


async def insert_message(game: Game):
    '''Cоздает запись результата игры в БД'''
    query = '''
        INSERT OR IGNORE INTO {} ( {} )
        VALUES ( {} )
    '''.format(
        GAME_TABLE_NAME,
        ','.join(game._fields),
        ','.join([f"'{value}'" for field, value in zip(game._fields, game._asdict().values())])
    )
    await commit(query)

async def insert_games(games: list[Game]):
    '''Cоздает записи результатов игр в БД'''
    fields = ','.join(Game._fields)
    values = ',\n'.join([ '('+', '.join(map(lambda x: f"'{x}'", game._asdict().values())) + ')' for game in games ])
 
    query = f'''
        INSERT OR IGNORE INTO {GAME_TABLE_NAME} ( {fields} )
        VALUES {values}
    '''
    await commit(query)

async def insert_user(user_id, username):
    '''Создание записи пользователя в БД'''
    query = '''
        INSERT OR IGNORE INTO {} (user_id, username)
        VALUES ('{}', '{}')
    '''.format(USERS_TABLE_NAME, user_id, username)
    await commit(query)


async def delete_game_by_game_id(game_id: int):
    '''Удаляет сообщение по id игры'''
    query = f"DELETE FROM {GAME_TABLE_NAME} WHERE game_id = '{game_id}'"
    await commit(query)
    

async def delete_games_by_game_ids(game_ids: list[int]):
    query = f"DELETE FROM {GAME_TABLE_NAME} WHERE game_id IN ({', '.join(map(str, game_ids))})"
    await commit(query)


async def delete_last_messages(delete_games_count=5) -> int:
    if delete_games_count != 0:
        last_games = await get_some_games(-delete_games_count)
        games_ids = [game['game_id'] for game in last_games]
        await delete_games_by_game_ids(games_ids)
        # for game in last_games:
        #     await delete_game_by_game_id(game['game_id'])
        #     game_id = game['game_id']
        #     logger.info(f'Удален пост: {game_id}')
    last_game = await get_some_games(-1)
    return last_game[0]['game_id'] if last_game else 0 # type: ignore


async def get_some_games(count: int) -> Iterable[aiosqlite.Row]:
    '''Получить немного игр, желательно до 1000'''

    query1 = '''
    SELECT * FROM {}
    ORDER BY id DESC
    LIMIT {};
    '''
    query2 = '''
    SELECT * FROM {}
    LIMIT {};
    '''
    if count<0:
        query = query1.format(GAME_TABLE_NAME, -count)
    elif count>0:
        query = query2.format(GAME_TABLE_NAME, count)
    else:
        query = query1.format(GAME_TABLE_NAME, 1)
    return await fetch(query)

async def get_some_filter_games(count: int, field: str, value: str):
    '''Получить немного игр, желательно до 1000'''
    # Получение сообщений из таблицы
    query1 = '''
    SELECT * FROM {}
    WhERE {} = '{}'
    ORDER BY id DESC
    LIMIT {};
    '''
    query2 = '''
    SELECT * FROM {}
    WhERE {} = '{}'
    LIMIT {};
    '''
    if count<0:
        query = query1.format(GAME_TABLE_NAME, field, value, -count)
    elif count>0:
        query = query2.format(GAME_TABLE_NAME, field, value, count)
    else:
        query = query1.format(GAME_TABLE_NAME, field, value, 1)
    return await fetch(query)

async def get_many_games(count: int|str='all'):
    '''Получить много игр, больше 1000, возвращает генератор списками по 1000 игр'''
    query = ''
    if count == 'all':
        query = f'SELECT * FROM {GAME_TABLE_NAME}'
    elif count == '-all':
        query = f'SELECT * FROM {GAME_TABLE_NAME} ORDER BY id DESC'
    elif count > 0: # type: ignore
        query = f'SELECT * FROM {GAME_TABLE_NAME} LIMIT {count}'
    elif count < 0: # type: ignore
        query = f'SELECT * FROM {GAME_TABLE_NAME} ORDER BY id DESC LIMIT {count}'
    elif count == 0:
        query = f'SELECT * FROM {GAME_TABLE_NAME} ORDER BY id DESC LIMIT 1'
    if query:
        async for game in fetchmany(query):
            yield game
    

async def get_users():
    query = 'SELECT * FROM {}'.format(USERS_TABLE_NAME)
    return await fetch(query)

async def init_db():
    logger.info('START DATABASE INIT')
    logger.info('CREATE TABLES')
    await create_tables()
    logger.info('DATABASE INIT SUCCESSFUL')

async def test():
    async for game in get_many_games():
        print(game)
        break


async def main():
    # test_game = Game(
    #     game_id=618, 
    #     game_date=str(datetime.date(2020, 3, 13)), 
    #     game_time=str(datetime.time(1, 25)), 
    #     p1_name='КунгДжин', 
    #     p2_name='Скорпион', 
    #     p1_game_win_coef=None, 
    #     p2_game_win_coef=None, 
    #     p1_round_win_coef=1.78, 
    #     p2_round_win_coef=2.135, 
    #     f_coef=None, b_coef=None, 
    #     r_coef=None, 
    #     min_num_total=27.5, 
    #     min_num_total_min_coef=3.7, 
    #     min_num_total_max_coef=1.288, 
    #     mid_num_total=33.5, 
    #     mid_num_total_min_coef=2.025, 
    #     mid_num_total_max_coef=1.88, 
    #     max_num_total=39.5, 
    #     max_num_total_min_coef=1.288, 
    #     max_num_total_max_coef=3.7, 
    #     fyes=None, fno=None, 
    #     p1_wins=2, p2_wins=1, 
    #     round1_winner='P1', 
    #     round1_finish='R', 
    #     round1_time=37, 
    #     round1_total=None, 
    #     round2_winner='P1', 
    #     round2_finish='R', 
    #     round2_time=32, 
    #     round2_total=None, 
    #     round3_winner='P2', 
    #     round3_finish='F', 
    #     round3_time=37, 
    #     round3_total=None, 
    #     round4_winner='P2', 
    #     round4_finish='R', 
    #     round4_time=21, 
    #     round4_total=None, 
    #     round5_winner='P2', 
    #     round5_finish='R', 
    #     round5_time=18, 
    #     round5_total=None, 
    #     round6_winner='P1', 
    #     round6_finish='F', 
    #     round6_time=43, 
    #     round6_total=None, 
    #     round7_winner='P1', 
    #     round7_finish='F', 
    #     round7_time=14, 
    #     round7_total=None, 
    #     round8_winner='P2', 
    #     round8_finish='R', 
    #     round8_time=24, 
    #     round8_total=None, 
    #     round9_winner='P2',
    #     round9_finish='F', 
    #     round9_time=15, 
    #     round9_total=None
    # )
    # users = await get_users()
    # print(users)
    # print(type(users))

    # games = await get_all_games()
    async for game in get_many_games():
        print(game)
        break
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
