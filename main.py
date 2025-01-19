import asyncio
import logging
import sys
from datetime import datetime
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from app.database.db_requests import get_all_trainings, deactive_training
from app.database.models import async_main
from app.handlers.info_update_handler import router as router1
from app.handlers.registration_handler import router as router2
from app.handlers.training_handler import router as router3
from app.handlers.static_handler import router as router4

dp = Dispatcher()
load_dotenv()
TOKEN = getenv('TOKEN')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))


async def notify_users():
    trainings = await get_all_trainings()
    for training in trainings:
        print(training.time)
        now = datetime.now()
        diff = now - training.time
        minute_passed = diff.total_seconds() / 60
        print(minute_passed)
        if abs(minute_passed) <= 30:
            await bot.send_message(chat_id=training.tg_id,
                                   text=f"Напоминаю, что через 30 минут у вас тренировка ({training.type})!")
            await deactive_training(training.id)


async def main():
    commands = [BotCommand(command='my_info', description='Информация о Вас'),
                BotCommand(command='set_aim', description='Установить цель своих тренировок'),
                BotCommand(command='set_age', description='Сменить возраст'),
                BotCommand(command='set_weight', description='Сменить вес'),
                BotCommand(command='set_height', description='Сменить рост'),
                BotCommand(command='set_plan', description='Добавить тренироку в свое расписание'),
                BotCommand(command='view_plan', description='Посмотреть список запланированных тренировок'),
                BotCommand(command='view_plan', description='Посмотреть список запланированных тренировок'),
                BotCommand(command='get_advice', description='Получить совет по составлению расписания'),
                BotCommand(command='menu', description='Меню'),
                ]
    dp.include_router(router1)
    dp.include_router(router2)
    dp.include_router(router3)
    dp.include_router(router4)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify_users, CronTrigger(minute="*"))
    scheduler.start()
    try:
        await bot.set_my_commands(commands, BotCommandScopeDefault())
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(async_main())
    asyncio.run(main())
