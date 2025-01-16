import time
from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.database.db_requests import get_user, set_training, get_trainings
from app.middlewares.logger_middleware import LoggerMiddleware
from app.middlewares.registartion_middleware import RegistrationMiddleware
from app.utils import get_advice, text_with_trainings, check_conditions

router = Router()
router.message.middleware(RegistrationMiddleware())
router.message.middleware(LoggerMiddleware())


class PlanState(StatesGroup):
    date = State()
    time = State()
    training_type = State()


class ConditionsState(StatesGroup):
    condition = State()


@router.message(Command('set_plan'))
async def set_plan_command(message: Message, state: FSMContext):
    await message.answer("Введите дату тренировки в формате день/месяц/год:")
    await state.set_state(PlanState.date)


@router.message(PlanState.date)
async def set_date(message: Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%d/%m/%Y")
        await state.update_data(date=message.text)
        await state.set_state(PlanState.time)
        await message.answer("Введите время суток тренировки в формате часы:минуты")
    except Exception as e:
        await message.answer("Вы ввели дату в неверном формате, попробуйте заново.")
        await state.clear()


@router.message(PlanState.time)
async def set_time(message: Message, state: FSMContext):
    try:
        time.strptime(message.text, "%H:%M")
        await state.update_data(time=message.text)
        await state.set_state(PlanState.training_type)
        await message.answer("Введите тип тренировки:")
    except Exception as e:
        await message.answer("Вы ввели время в неверном формате, попробуйте заново.")
        await state.clear()


@router.message(PlanState.training_type)
async def set_training_type(message: Message, state: FSMContext):
    await state.update_data(training_type=message.text)
    data = await state.get_data()
    await set_training(message.from_user.id, data["date"], data["time"], data["training_type"])
    await message.answer("Тренировка успешно сохранена.")
    await state.clear()


@router.message(Command('view_plan'))
async def view_plan_command(message: Message):
    trainings = await get_trainings(message.from_user.id)
    answer = text_with_trainings(trainings)
    await message.answer(text=f"Ваши запланированные тренировки:\n{answer}")


@router.message(Command("get_advice"))
async def get_advice_command(message: Message, state: FSMContext):
    await state.set_state(ConditionsState.condition)
    await message.answer("Введите свое физическое состояние, опишите травмы, как вы себя чувствуете:")


@router.message(ConditionsState.condition)
async def get_advice_with_condition(message: Message, state: FSMContext):
    if check_conditions(message.text):
        await state.update_data(condition=message.text)
        data = await state.get_data()
        user = await get_user(message.from_user.id)
        trainings = await get_trainings(message.from_user.id)
        trainings_text = text_with_trainings(trainings)
        advice = get_advice(user.sex, user.age, user.height, user.weight, user.aim, data["condition"], trainings_text)
        await message.answer(advice)
    else:
        await message.answer("Вы не описали свое физическое состояние, попробуйте заново.")
