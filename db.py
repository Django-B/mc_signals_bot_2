import aiosqlite, asyncio
import datetime
import time


from get_config import get_config
from telethon_client import user_client

from named_tuples import Game

config = get_config()

DB_NAME = config['db_name']
BOT_OWNERS = config['bot_owners'].split()
# CHANNEL_NAME = config['target_channel_url'].split('/')[-1]
GAME_TABLE_NAME = 'game'
USERS_TABLE_NAME = 'bot_user'


async def create_tables():
    # with open(DB_NAME, 'w'): pass
    async with aiosqlite.connect(DB_NAME) as db:
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
    async with aiosqlite.connect(DB_NAME) as db:
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

        await db.commit()

async def insert_user(user_id, username):
    '''Создание записи пользователя в БД'''
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.cursor()

        # Вставка данных сообщения в таблицу
        await cursor.execute('''
            INSERT OR IGNORE INTO {} (user_id, username)
            VALUES (?, ?)
        '''.format(USERS_TABLE_NAME), (user_id, username))

        await db.commit()

async def insert_users_from_config():
    '''Добавление всех пользователей перечисленных в config.ini->BOT_OWNERS в БД'''
    for username in BOT_OWNERS:
        user_id = (await user_client.get_entity(username)).id
        await insert_user(user_id, username)

async def delete_game_by_note_id(note_id: int):
    '''Удаляет сообщение по id записи'''
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.cursor()
        
        await cursor.execute(f"DELETE FROM {GAME_TABLE_NAME} WHERE id = ?", (note_id,))
        await db.commit()
        deleted_rows_count = cursor.rowcount
        await cursor.close()
    return deleted_rows_count

async def delete_last_messages(delete_messages_count=5) -> int:
    messages_history = await get_messages()
    last_message_id = messages_history[-1]['id']
    for _ in range(delete_messages_count):
        await delete_game_by_note_id(last_message_id)
        print(f'Удален пост:', last_message_id)
        last_message_id -= 1

    return last_message_id


async def get_messages() -> Game:
    async with aiosqlite.connect(DB_NAME) as db:
        # db.row_factory = aiosqlite.Row
        cursor = await db.cursor()

        # Получение всех сообщений из таблицы
        await cursor.execute(f'SELECT * FROM {GAME_TABLE_NAME}')
        messages = await cursor.fetchall()

        # return (messages)
        return list(map(lambda x: Game(*x[1:]), messages))

async def get_users() -> list:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.cursor()

        # Получение всех сообщений из таблицы
        await cursor.execute('SELECT * FROM {}'.format(USERS_TABLE_NAME))
        users = await cursor.fetchall()

        return list(users)

async def init_db():
    print('START DATABASE INIT')
    print('CREATE TABLES')
    await create_tables()
    print('INSERT USERS FROM CONFIG')
    await insert_users_from_config()
    print('DATABASE INIT SUCCESSFUL')


async def main():
    test_game = Game(
        message_id=618, 
        game_date=str(datetime.date(2020, 3, 13)), 
        game_time=str(datetime.time(1, 25)), 
        p1_name='КунгДжин', 
        p2_name='Скорпион', 
        p1_game_win_coef=None, 
        p2_game_win_coef=None, 
        p1_round_win_coef=1.78, 
        p2_round_win_coef=2.135, 
        f_coef=None, b_coef=None, 
        r_coef=None, 
        min_num_total=27.5, 
        min_num_total_min_coef=3.7, 
        min_num_total_max_coef=1.288, 
        mid_num_total=33.5, 
        mid_num_total_min_coef=2.025, 
        mid_num_total_max_coef=1.88, 
        max_num_total=39.5, 
        max_num_total_min_coef=1.288, 
        max_num_total_max_coef=3.7, 
        fyes=None, fno=None, 
        p1_wins=2, p2_wins=1, 
        round1_winner='P1', 
        round1_finish='R', 
        round1_time=37, 
        round1_total=None, 
        round2_winner='P1', 
        round2_finish='R', 
        round2_time=32, 
        round2_total=None, 
        round3_winner='P2', 
        round3_finish='F', 
        round3_time=37, 
        round3_total=None, 
        round4_winner='P2', 
        round4_finish='R', 
        round4_time=21, 
        round4_total=None, 
        round5_winner='P2', 
        round5_finish='R', 
        round5_time=18, 
        round5_total=None, 
        round6_winner='P1', 
        round6_finish='F', 
        round6_time=43, 
        round6_total=None, 
        round7_winner='P1', 
        round7_finish='F', 
        round7_time=14, 
        round7_total=None, 
        round8_winner='P2', 
        round8_finish='R', 
        round8_time=24, 
        round8_total=None, 
        round9_winner='P2',
        round9_finish='F', 
        round9_time=15, 
        round9_total=None
    )
    await init_db()
    # await insert_message(test_game)
    start_time = time.time()
    msgs = await get_messages()
    end_time = time.time()
    execute_time = start_time-end_time
    print(msgs[0])
    print(execute_time)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
