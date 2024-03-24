from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from logger import logger

import signals
from history import dump_channel_history
from telethon_client import user_client
from db import get_users, init_db, insert_user

from get_config import get_config

config = get_config()

API_TOKEN = config['bot_token']
CHECK_INTERVAL = float(config['check_interval'])*60
BOT_OWNERS = config['bot_owners'].split()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который отправляет сигналы для ставок Mortal Combat", reply_markup=reply_keyboard)

async def send_signal():
    pass

async def schedule_check_strategies():
    users = await get_users()
    while True:
        logger.info('Загрузка новых сообщений')
        await dump_channel_history()
        logger.info('Проверка сигналов')
        all_signals = await signals.check_all_signals()
        if all_signals:
            logger.info('Есть сигнал')
            for signal in all_signals:
                for user_id, username in users:
                    logger.info(f'Отправка сигнала пользователю {username}')
                    await bot.send_message(chat_id=user_id, text=signal, parse_mode=ParseMode.MARKDOWN)
        logger.info('Конец проверки сигналов'.center)
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
    logger.info('Инициализация базы данных')
    await init_db()
    logger.info('База данных успешно инициализирована')

    logger.info('Проверка списка пользователей бота')
    user_ids = await insert_users_from_config()
    for user_id in user_ids:
        await bot.send_message(user_id, 'Бот запущен!')
    logger.info('Бот успешно запущен'.center(100, '-'))

    loop = asyncio.get_event_loop()
    loop.create_task(schedule_check_strategies())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)