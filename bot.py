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
from named_tuples import max_round_total_streak

from get_config import get_config

config = get_config()

API_TOKEN = config['bot_token']
CHECK_INTERVAL = float(config['check_interval'])*60
BOT_OWNERS = config['bot_owners'].split()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    button1 = KeyboardButton('Макс. серия TB')
    button2 = KeyboardButton('Макс. серия TM')
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(button1)
    reply_markup.add(button2)
    await message.reply("Привет! Я бот, который отправляет сигналы для ставок Mortal Combat", reply_markup=reply_markup)

@dp.message_handler()
async def messages_handler(msg: types.Message):
    if msg.text == 'Макс. серия TB':
        message = await msg.answer('Маск. серия TB:')
        games = lambda: get_many_games('all')
        round1 = await max_round_total_streak(games, 'TB', 1)
        message = await message.edit_text(message.text+f'\nРаунд 1 => {round1.streak}')
        round2 = await max_round_total_streak(games, 'TB', 2)
        message = await message.edit_text(message.text+f'\nРаунд 2 => {round2.streak}')
        round3 = await max_round_total_streak(games, 'TB', 3)
        message = await message.edit_text(message.text+f'\nРаунд 3 => {round3.streak}')
        round4 = await max_round_total_streak(games, 'TB', 4)
        message = await message.edit_text(message.text+f'\nРаунд 4 => {round4.streak}')
        round5 = await max_round_total_streak(games, 'TB', 5)
        message = await message.edit_text(message.text+f'\nРаунд 5 => {round5.streak}\nГотово!')

        # res = 'Длины серий TB\n'+'\n'.join([
        #     'Раунд 1 => '+str(round1.streak),
        #     'Раунд 2 => '+str(round2.streak),
        #     'Раунд 3 => '+str(round3.streak),
        #     'Раунд 4 => '+str(round4.streak),
        #     'Раунд 5 => '+str(round5.streak),
        # ])
        # await msg.reply(res, reply=False)
    elif msg.text == 'Макс. серия TM':
        message = await msg.answer('Маск. серия TM:')
        games = lambda: get_many_games('all')
        round1 = await max_round_total_streak(games, 'TM', 1)
        await message.edit_text(message.text+f'\nРаунд 1 => {round1.streak}')
        round2 = await max_round_total_streak(games, 'TM', 2)
        await message.edit_text(message.text+f'\nРаунд 2 => {round2.streak}')
        round3 = await max_round_total_streak(games, 'TM', 3)
        await message.edit_text(message.text+f'\nРаунд 3 => {round3.streak}')
        round4 = await max_round_total_streak(games, 'TM', 4)
        await message.edit_text(message.text+f'\nРаунд 4 => {round4.streak}')
        round5 = await max_round_total_streak(games, 'TM', 5)
        await message.edit_text(message.text+f'\nРаунд 5 => {round5.streak}\nГотово!')

        # res = 'Длины серий TM\n'+'\n'.join([
        #     'Раунд 1 => '+str(round1.streak),
        #     'Раунд 2 => '+str(round2.streak),
        #     'Раунд 3 => '+str(round3.streak),
        #     'Раунд 4 => '+str(round4.streak),
        #     'Раунд 5 => '+str(round5.streak),
        # ])
        # await msg.reply(res, reply=False)
    

async def schedule_check_strategies():
    users = await get_users()
    while True:
        await dump_channel_history()
        logger.info('Проверка сигналов')
        all_signals = await signals.check_all_signals()
        if all_signals:
            logger.info('Есть сигнал')
            for signal in all_signals:
                for user_id, username in users:
                    logger.info(f'Отправка сигнала пользователю {username}')
                    try:
                        with open('bot_history.json', 'r') as f:
                            send = json.load(f)['last_msg'] != signal
                    except:
                        pass
                    await bot.send_message(chat_id=user_id, text=signal, parse_mode=ParseMode.MARKDOWN)
                    with open('bot_history.json', 'w') as f:
                        json.dump({'last_msg': signal}, а)

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
