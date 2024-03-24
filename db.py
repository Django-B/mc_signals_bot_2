import aiosqlite, asyncio
import datetime
import time
from logger import logger
from get_config import get_config

from named_tuples import Game, Games

config = get_config()

DB_NAME = config['db_name']
# CHANNEL_NAME = config['target_channel_url'].split('/')[-1]
GAME_TABLE_NAME = 'game'
USERS_TABLE_NAME = 'bot_user'


async def create_tables():
    # with open(DB_NAME, 'w'): pass
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        cursor = await db.cursor()

        with open('game.sql') as f:
            game_table_query = f.read()
        with open('owner.sql') as f:
            owner_table_query = f.read()

        await cursor.execute(game_table_query)
        await cursor.execute(owner_table_query)

        await db.commit()

async def insert_message(game: Game):
    '''Cоздает запись результата игры в БД'''
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        cursor = await db.cursor()

        # Вставка данных сообщения в таблицу
        await cursor.execute('''
            INSERT OR IGNORE INTO {} ( {} )
            VALUES ( {} )
        '''.format(
                GAME_TABLE_NAME,
                ','.join(game._fields),
                ','.join(['?' for _ in game._fields])
            ), list(game)
        )

        if game.p1_name == 'Чужой' and game.p2_name == 'Эрмак':
            logger.info(game)

        await db.commit()

async def insert_user(user_id, username):
    '''Создание записи пользователя в БД'''
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        cursor = await db.cursor()

        # Вставка данных сообщения в таблицу
        await cursor.execute('''
            INSERT OR IGNORE INTO {} (user_id, username)
            VALUES (?, ?)
        '''.format(USERS_TABLE_NAME), (user_id, username))

        await db.commit()



async def delete_game_by_game_id(game_id: int):
    '''Удаляет сообщение по id игры'''
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        cursor = await db.cursor()
        
        await cursor.execute(f"DELETE FROM {GAME_TABLE_NAME} WHERE game_id = ?", (game_id,))
        await db.commit()
        deleted_rows_count = cursor.rowcount
        await cursor.close()
    return deleted_rows_count

async def delete_last_messages(delete_games_count=5) -> int:
    if delete_games_count != 0:
        last_games = await get_some_games(-delete_games_count)
        for game in last_games:
            await delete_game_by_game_id(game['game_id'])
            game_id = game['game_id']
            logger.info(f'Удален пост: {game_id}')
    last_game = await get_some_games(-1)
    return last_game[0]['game_id']


async def get_some_games(count: int) -> Games:
    '''Получить немного игр, желательно до 1000'''
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.cursor()

        # Получение сообщений из таблицы
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
        await cursor.execute(query)
        games = await cursor.fetchall()

        return games
async def get_many_games(count: int|str='all',batch_size: int=50):
    '''Получить много игр, больше 1000, возвращает генератор списками по 1000 игр'''
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.cursor()
        if count == 'all':
            await cursor.execute(f'SELECT * FROM {GAME_TABLE_NAME}')
        elif count == '-all':
            await cursor.execute(f'SELECT * FROM {GAME_TABLE_NAME} ORDER BY id DESC')
        elif count > 0:
            await cursor.execute(f'SELECT * FROM {GAME_TABLE_NAME} LIMIT {count}')
        elif count < 0:
            await cursor.execute(f'SELECT * FROM {GAME_TABLE_NAME} ORDER BY id DESC LIMIT {count}')
        elif count == 0:
            await cursor.execute(f'SELECT * FROM {GAME_TABLE_NAME} ORDER BY id DESC LIMIT 1')

        while True:
            rows = await cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows


async def get_users() -> list:
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        # db.row_factory = aiosqlite.Row
        cursor = await db.cursor()

        # Получение всех сообщений из таблицы
        await cursor.execute('SELECT * FROM {}'.format(USERS_TABLE_NAME))
        users = await cursor.fetchall()

        return users

async def init_db():
    logger.info('START DATABASE INIT')
    logger.info('CREATE TABLES')
    await create_tables()
    logger.info('DATABASE INIT SUCCESSFUL')

async def test():
    games = get_many_games()
    async for game in games:
        # print(game)
        pass



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
    await test()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
