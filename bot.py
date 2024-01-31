from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import asyncio

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
        print('Загрузка новых сообщений'.center(100, '-'))
        await dump_channel_history()
        print('Проверка сигналов'.center(100, '-'))
        all_signals = await signals.check_all_signals()
        if all_signals:
            print('Есть сигнал'.center(100, '-'))
            for signal in all_signals:
                for user_id, username in users:
                    print(f'Отправка сигнала пользователю {username}'.center(100, '-'))
                    await bot.send_message(chat_id=user_id, text=signal, parse_mode=ParseMode.MARKDOWN)
        print(f'Конец проверки сигналов {username}'.center(100, '-'))
        await asyncio.sleep(CHECK_INTERVAL)

async def insert_users_from_config():
    '''Добавление всех пользователей перечисленных в config.ini->BOT_OWNERS в БД'''
    for username in BOT_OWNERS:
        user_id = (await user_client.get_entity(username)).id
        await insert_user(user_id, username)

async def on_startup(_):
    print('Проверка списка пользователей бота'.center(100, '-'))
    await insert_users_from_config()
    print('Бот успешно запущен'.center(100, '-'))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_check_strategies())

    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)