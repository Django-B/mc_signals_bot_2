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
from analytics import max_f_streak

from get_config import get_config, get_or_create_config

config = get_config()

API_TOKEN = config['bot_token']
CHECK_INTERVAL = float(config['check_interval'])*60 # type: ignore
BOT_OWNERS = config['bot_owners'].split()

bot = Bot(token=API_TOKEN) # type: ignore
dp = Dispatcher(bot)

async def set_bot_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),

        types.BotCommand("ochka", "5 тб и 5 тб у обоих персонажей перед их очкой"),

        types.BotCommand("max_f", "Макс. серия фаталити"),
        types.BotCommand("set_f_limit", "Изменить мин. серию Fаталити"),

        types.BotCommand("set_tb_streak_limit", "Изменить переменную tb_streak_limit"),
        types.BotCommand("set_tbb_streak_limit", "Изменить переменную tbb_streak_limit"),
        types.BotCommand("set_tbbb_streak_limit", "Изменить переменную tbbb_streak_limit"),
        types.BotCommand("set_tm_streak_limit", "Изменить переменную tm_streak_limit"),
        types.BotCommand("set_tmm_streak_limit", "Изменить переменную tmm_streak_limit"),
        types.BotCommand("set_tmmm_streak_limit", "Изменить переменную tmmm_streak_limit"),

        types.BotCommand("max_tb", "Макс. серия TB"),
        types.BotCommand("max_tbb", "Макс. серия TBB"),
        types.BotCommand("max_tbbb", "Макс. серия TBBB"),
        types.BotCommand("max_tm", "Maкс. серия ТМ"),
        types.BotCommand("max_tmm", "Maкс. серия ТММ"),
        types.BotCommand("max_tmmm", "Maкс. серия ТМММ"),
        types.BotCommand("max_tm", "Maкс. серия ТМ"),

        types.BotCommand("streak_tb1", "Статистика ТБ 1 раунд"),
        types.BotCommand("streak_tbb1", "Статистика ТББ 1 раунд"),
        types.BotCommand("streak_tbbb1", "Статистика ТБББ 1 раунд"),
        types.BotCommand("streak_tm1", "Статистика ТМ 1 раунд"),
        types.BotCommand("streak_tmm1", "Статистика ТММ 1 раунд"),
        types.BotCommand("streak_tmmm1", "Статистика ТМММ 1 раунд"),

        types.BotCommand("streak_tb2", "Статистика ТБ 2 раунд"),
        types.BotCommand("streak_tbb2", "Статистика ТББ 2 раунд"),
        types.BotCommand("streak_tbbb2", "Статистика ТБББ 2 раунд"),
        types.BotCommand("streak_tm2", "Статистика ТМ 2 раунд"),
        types.BotCommand("streak_tmm2", "Статистика ТММ 2 раунд"),
        types.BotCommand("streak_tmmm2", "Статистика ТМММ 2 раунд"),

        types.BotCommand("streak_tb3", "Статистика ТБ 3 раунд"),
        types.BotCommand("streak_tbb3", "Статистика ТББ 3 раунд"),
        types.BotCommand("streak_tbbb3", "Статистика ТБББ 3 раунд"),
        types.BotCommand("streak_tm3", "Статистика ТМ 3 раунд"),
        types.BotCommand("streak_tmm3", "Статистика ТММ 3 раунд"),
        types.BotCommand("streak_tmmm3", "Статистика ТМММ 3 раунд"),

        types.BotCommand("streak_tb4", "Статистика ТБ 4 раунд"),
        types.BotCommand("streak_tbb4", "Статистика ТББ 4 раунд"),
        types.BotCommand("streak_tbbb4", "Статистика ТБББ 4 раунд"),
        types.BotCommand("streak_tm4", "Статистика ТМ 4 раунд"),
        types.BotCommand("streak_tmm4", "Статистика ТММ 4 раунд"),
        types.BotCommand("streak_tmmm4", "Статистика ТМММ 4 раунд"),

        types.BotCommand("streak_tb5", "Статистика ТБ 5 раунд"),
        types.BotCommand("streak_tbb5", "Статистика ТББ 5 раунд"),
        types.BotCommand("streak_tbbb5", "Статистика ТБББ 5 раунд"),
        types.BotCommand("streak_tm5", "Статистика ТМ 5 раунд"),
        types.BotCommand("streak_tmm5", "Статистика ТММ 5 раунд"),
        types.BotCommand("streak_tmmm5", "Статистика ТМММ 5 раунд"),
    ])

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который отправляет сигналы для ставок Mortal Combat")


'''
@dp.message_handler(commands=['set_streak_limit'])
async def set_streak_limit(msg: types.Message):
    print(msg.text)
    splt = msg.text.split(' ')
    val = splt[1] if len(splt) > 1 else ''

    str_limit = get_or_create_config('streak_limit', val)

    await msg.answer(f'{str_limit=}')
'''

@dp.message_handler(commands=['ochka'])
async def ochka(msg: types.Message):
    await msg.answer('Здесь должна быть статистика по очкам')


@dp.message_handler(lambda message: message.text.startswith('/set_'))
async def set_variable(msg: types.Message):
    print(msg.text)
    splt = msg.text.split(' ', 1)
    var = splt[0].split('_')[1]
    val = splt[1] if len(splt) > 1 else ''

    val_ = get_or_create_config(var, val)

    await msg.answer(f'{var}={val_}')


@dp.message_handler(commands=['max_f'])
async def max_f(msg: types.Message):
    message = await msg.answer('Макс. серия фаталити:')
    message_text=message.text
    print('get games')
    games = lambda: get_many_games('all')
    for i in range(1, 6):
        print('count streak', i)
        streak = await max_f_streak(games, i)
        message_text = message_text+f'\nРаунд {i} -> {streak}'
        message = await message.edit_text(message.text+f'\nРаунд {i} -> {streak}')
    message = await message.edit_text(message_text+'\n✅')


@dp.message_handler(lambda message: message.text.startswith('/max_T'))
async def max_tm(msg: types.Message):
    total_name = msg.text.split('_')[-1].upper()
    message = await msg.answer(f'Макс. серия {total_name}:')
    games = lambda: get_many_games('all')
    message_text = message.text
    for i in range(1, 6):
        round_streak = await max_round_total_streak(games, total_name, i)
        message_text = message_text+f'\nРаунд {i} -> {round_streak}'
        message = await message.edit_text(message.text+f'\nРаунд {i} -> {round_streak}')
        
    message = await message.edit_text(message_text+'\n✅')

@dp.message_handler(lambda message: message.text.startswith('/streak_'))
async def streak_tb(msg: types.Message):
    total_name = msg.text.split('_')[-1][:-1].upper()
    num = msg.text[-1]
    if num.isdigit() and int(num) > 0 and int(num) < 6:
        message = await msg.answer(f'Статистика по сериям {total_name} раунд {num}:') 
        games = lambda: get_many_games('all')

        stats = await get_total_streak_count(games, total_name, int(num))
        from pprint import pprint
        pprint(stats)
        answer_text = message.text
        for length, count in sorted(stats.items()):
            answer_text = answer_text+f'\nДлина серии {length} -> Кол-во {count}'
        answer_text = answer_text+'\n✅'
        message = await message.edit_text(answer_text)


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
