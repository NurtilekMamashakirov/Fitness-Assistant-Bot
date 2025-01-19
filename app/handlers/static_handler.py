from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.database.db_requests import get_user
from app.keybords import menu_keyboard
from app.middlewares.logger_middleware import LoggerMiddleware
from app.middlewares.registartion_middleware import RegistrationMiddleware

router = Router()
router.message.middleware(RegistrationMiddleware())
router.message.middleware(LoggerMiddleware())


@router.message(Command("my_info"))
@router.message(F.text == "Мой профиль")
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


@router.callback_query(F.data == "menu")
@router.message(Command("menu"))
async def menu_callback(callback: [CallbackQuery, Message]):
    if isinstance(callback, CallbackQuery):
        await callback.message.answer("В данном окне представлены действия, которые помогут вам упросить тренировки.",
                                      reply_markup=menu_keyboard)
    else:
        await callback.answer("В данном окне представлены действия, которые помогут вам упросить тренировки.",
                                      reply_markup=menu_keyboard)


@router.message()
async def unknown_command(message: Message):
    await message.answer(text="Неизвестная команда.")
