from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import sys
import json

import signals
from logger import logger
from history import dump_channel_history
from telethon_client import user_client
from db import get_users, init_db, insert_user, delete_last_messages, get_many_games
from named_tuples import max_round_total_streak, get_total_streak_count

from get_config import get_config

config = get_config()

API_TOKEN = config['bot_token']
CHECK_INTERVAL = float(config['check_interval'])*60
BOT_OWNERS = config['bot_owners'].split()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def set_bot_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("max_tb", "Макс. серия TB"),
        types.BotCommand("max_tm", "Maкс. серия ТМ"),
        types.BotCommand("streak_tb1", "Статистика ТБ 1 раунд"),
        types.BotCommand("streak_tm1", "Статистика ТМ 1 раунд"),
        types.BotCommand("streak_tb2", "Статистика ТБ 2 раунд"),
        types.BotCommand("streak_tm2", "Статистика ТМ 2 раунд"),
        types.BotCommand("streak_tb3", "Статистика ТБ 3 раунд"),
        types.BotCommand("streak_tm3", "Статистика ТМ 3 раунд"),
        types.BotCommand("streak_tb4", "Статистика ТБ 4 раунд"),
        types.BotCommand("streak_tm4", "Статистика ТМ 4 раунд"),
        types.BotCommand("streak_tb5", "Статистика ТБ 5 раунд"),
        types.BotCommand("streak_tm5", "Статистика ТМ 5 раунд"),
    ])

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который отправляет сигналы для ставок Mortal Combat")


@dp.message_handler(commands=['max_tb'])
async def max_tb(msg: types.Message):
    message = await msg.answer('Макс. серия TB:')
    games = lambda: get_many_games('all')
    for i in range(1, 6):
        round_streak = await max_round_total_streak(games, 'TB', i)
        message = await message.edit_text(message.text+f'\nРаунд {i} -> {round_streak}')
        
    message = await message.edit_text(message.text+'\n✅')

@dp.message_handler(commands=['max_tm'])
async def max_tm(msg: types.Message):
    message = await msg.answer('Макс. серия TM:')
    games = lambda: get_many_games('all')
    message_text = message.text
    for i in range(1, 6):
        round_streak = await max_round_total_streak(games, 'TM', i)
        message_text = message_text+f'\nРаунд {i} -> {round_streak}'
        message = await message.edit_text(message.text+f'\nРаунд {i} -> {round_streak}')
        
    message = await message.edit_text(message_text+'\n✅')

@dp.message_handler(lambda message: message.text.startswith('/streak_tb'))
async def streak_tb(msg: types.Message):
    print('strek_tb')
    num = msg.text[-1]
    if num.isdigit() and int(num) > 0 and int(num) < 6:
        message = await msg.answer('Статистика по сериям TB:') 
        games = lambda: get_many_games('all')

        message = await message.edit_text(message.text+f'\nРаунд {num}:')

        stats = await get_total_streak_count(games, 'TB', int(num))
        for length, count in sorted(stats.items()):
            message = await message.edit_text(message.text+f'\nДлина серии {length} -> Кол-во {count}')
            
        message = await message.edit_text(message.text+'\n✅')

@dp.message_handler(lambda message: message.text.startswith('/streak_tm'))
async def messages_handler(msg: types.Message):
    print('strek_tm')
    
    num = msg.text[-1]
    if num.isdigit() and int(num) > 0 and int(num) < 6:
        message = await msg.answer('Статистика по сериям TM:') 
        games = lambda: get_many_games('all')
        
        message = await message.edit_text(message.text+f'\nРаунд {num}:')

        stats = await get_total_streak_count(games, 'TM', int(num))
        for length, count in sorted(stats.items()):
            message = await message.edit_text(message.text+f'\nДлина серии {length} -> Кол-во {count}')

        message = await message.edit_text(message.text+'\n✅')



async def schedule_check_strategies():
    last_signals_limit = 1000
    users = await get_users()
    while True:
        await dump_channel_history()
        logger.info('Проверка сигналов')
        all_signals = await signals.check_all_signals()

        # read signals
        try:
            with open('bot_history.json', 'r') as f:
                last_signals = json.load(f)['last_signals']
        except FileNotFoundError:
            last_signals = []

        plus_signals = []
        
        if all_signals:
            logger.info('Есть сигнал')
            for signal in all_signals:
                logger.info(signal)
                for user_id, username in users:
                    logger.info(f'Отправка сигнала пользователю {username}')
                    if not signal in last_signals:
                        await bot.send_message(chat_id=user_id, text=signal, parse_mode=ParseMode.MARKDOWN)

                        plus_signals.append(signal)
                        
                        
        new_last_signals = last_signals + plus_signals
        if len(new_last_signals) > last_signals_limit:
            del new_last_signals[:len(new_last_signals)-last_signals_limit]

        with open('bot_history.json', 'w') as f:
            json.dump({'last_signals': new_last_signals}, f)

        logger.info('Конец проверки сигналов')
        await asyncio.sleep(CHECK_INTERVAL)

async def insert_users_from_config():
    '''Добавление всех пользователей перечисленных в config.ini->BOT_OWNERS в БД'''
    user_ids = []
    for username in BOT_OWNERS:
        user_id = (await user_client.get_entity(username)).id
        await insert_user(user_id, username)
        user_ids.append(user_id)
    return user_ids

async def on_startup(_):
    await set_bot_commands(dp)
    logger.info('Инициализация базы данных')
    await init_db()
    logger.info('База данных успешно инициализирована')

    logger.info('Проверка списка пользователей бота')
    user_ids = await insert_users_from_config()
    for user_id in user_ids:
        await bot.send_message(user_id, 'Бот запущен!')
    logger.info('Бот успешно запущен')

    logger.info('Загрузка новых сообщений')

    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        await delete_last_messages(int(sys.argv[1]))

    loop = asyncio.get_event_loop()
    loop.create_task(schedule_check_strategies())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
