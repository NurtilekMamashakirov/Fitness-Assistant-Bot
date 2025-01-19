from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.database.db_requests import get_user, update_aim, update_age, update_weight, update_height
from app.middlewares.logger_middleware import LoggerMiddleware
from app.middlewares.registartion_middleware import RegistrationMiddleware
from app.utils import check_aim, check_age, check_height, check_weight

router = Router()
router.message.middleware(RegistrationMiddleware())
router.message.middleware(LoggerMiddleware())


class UpdateState(StatesGroup):
    age = State()
    weight = State()
    height = State()
    aim = State()


@router.message(Command("set_aim"))
async def set_aim_command(message: Message, state: FSMContext):
    await state.set_state(UpdateState.aim)
    await message.answer("Введите новую цель тренировок и не забудьте написать ваш текущий опыт.")


@router.message(UpdateState.aim)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(aim=message.text)
    data = await state.get_data()
    if check_aim(data["aim"]):
        await update_aim(tg_id=message.from_user.id, aim=data["aim"])
        await message.answer("Цель успешно обновлена!")
        await state.clear()
    else:
        await message.answer("Вы не описали цель или опыт. Попробуйте заново.")


@router.message(Command("set_age"))
async def set_aim_command(message: Message, state: FSMContext):
    await state.set_state(UpdateState.aim)
    await message.answer("Введите, сколько вам сейчас лет:")


@router.message(UpdateState.age)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    if check_age(data["age"]):
        await update_age(tg_id=message.from_user.id, age=data["age"])
        await message.answer("Возраст успешно обновлен!")
        await state.clear()
    else:
        await message.answer("Введенный возраст не корректен. Попробуйте заново.")


@router.message(Command("set_weight"))
async def set_aim_command(message: Message, state: FSMContext):
    await state.set_state(UpdateState.weight)
    await message.answer("Введите, сколько вы весите:")


@router.message(UpdateState.weight)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if check_weight(data["weight"]):
        await update_weight(tg_id=message.from_user.id, weight=data["weight"])
        await message.answer("Вес успешно обновлен!")
        await state.clear()
    else:
        await message.answer("Введенный вес не корректен. Попробуйте заново.")


@router.message(Command("set_height"))
async def set_aim_command(message: Message, state: FSMContext):
    await state.set_state(UpdateState.height)
    await message.answer("Введите, какой у вас рост:")


@router.message(UpdateState.height)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    data = await state.get_data()
    if check_height(data["height"]):
        await update_height(tg_id=message.from_user.id, height=data["height"])
        await message.answer("Рост успешно обновлен!")
        await state.clear()
    else:
        await message.answer("Введенный рост не корректен. Попробуйте заново.")
