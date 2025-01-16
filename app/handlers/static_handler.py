from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.db_requests import get_user
from app.middlewares.logger_middleware import LoggerMiddleware
from app.middlewares.registartion_middleware import RegistrationMiddleware

router = Router()
router.message.middleware(RegistrationMiddleware())
router.message.middleware(LoggerMiddleware())


@router.message(Command("my_info"))
async def my_info(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        sex_decoder = {"male": "Мужской", "female": "Женский"}
        answer = (f"Информация о вас: \n"
                  f"Возраст: {user.age}\nПол: {sex_decoder[user.sex]}\nРост: {user.height}\n"
                  f"Вес: {user.weight}\nЦель и опыт: {user.aim}")
        await message.answer(answer)
    else:
        await message.answer("Первым делом зарегестрируйтесь!")
