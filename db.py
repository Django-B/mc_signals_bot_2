import aiosqlite, asyncio
from pprint import pprint

from get_config import get_config
from telethon_client import user_client

from named_tuples import Game

config = get_config()

DB_NAME = config['db_name']
BOT_OWNERS = config['bot_owners'].split()
# CHANNEL_NAME = config['target_channel_url'].split('/')[-1]
GAME_TABLE_NAME = 'game'
OWNER_TABLE_NAME = 'owner'


async def insert_game(game: Game):
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
            ), (
                list(game)
            )
        )

        await db.commit()

async def insert_user(user_id, username):
    '''Создание записи пользователя в БД'''
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.cursor()

        # Вставка данных сообщения в таблицу
        await cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username)
            VALUES (?, ?)
        ''', (user_id, username))

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

async def delete_nlast_games(delete_messages_count=5) -> int:
    messages_history = await get_messages()
    last_message_id = messages_history[-1]['id']
    for _ in range(delete_messages_count):
        await delete_game_by_note_id(last_message_id)
        print(f'Удален пост:', last_message_id)
        last_message_id -= 1

    return last_message_id


async def get_messages() -> list:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.cursor()

        # Получение всех сообщений из таблицы
        await cursor.execute(f'SELECT * FROM {GAME_TABLE_NAME} WHERE message_text IS NOT NULL')
        messages = await cursor.fetchall()

        return list(messages)

async def get_users() -> list:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.cursor()

        # Получение всех сообщений из таблицы
        await cursor.execute('SELECT * FROM users')
        users = await cursor.fetchall()

        return list(users)

async def init_db():
    print('START DATABASE INIT')
    print('CREATE CHANNEL MESSAGES HISTORY TABLE')
    await create_channel_messages_table()
    print('CREATE USERS TABLE')
    await create_users_table()
    print('INSERT USERS FROM CONFIG')
    await insert_users_from_config()
    print('DATABASE INIT SUCCESSFUL')


async def main():
    await init_db()
    pprint((await get_messages())[100][''])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




