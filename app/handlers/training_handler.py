from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale

from app.database.db_requests import get_user, get_trainings, set_training
from app.keybords import get_time_keyboard, TimeCallbackData
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


@router.message(Command("set_plan"))
@router.message(F.text == "Запланировать тренировку")
async def set_plan(message: Message):
    calendar = SimpleCalendar(
        locale=await get_user_locale(message.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime.today(), datetime(2025, 12, 31))
    await message.answer(
        "Выберите: ",
        reply_markup=await calendar.start_calendar(year=datetime.today().year, month=datetime.today().month)
    )


# simple calendar usage - filtering callbacks of calendar format
@router.callback_query(SimpleCalendarCallback.filter())
async def set_date(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(datetime.today().year, datetime.today().month, datetime.today().day),
                             datetime(datetime.today().year + 1, datetime.today().month, datetime.today().day))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date=date.strftime("%Y-%m-%d"))
        await callback_query.message.answer(text="Выберите время:",
                                            reply_markup=get_time_keyboard(
                                                date=date))


@router.callback_query(TimeCallbackData.filter())
async def set_time(callback_query: CallbackQuery, state: FSMContext, callback_data: CallbackData):
    time = callback_data.value.replace(";", ":")
    await state.update_data(time=time)
    await state.set_state(PlanState.training_type)
    await callback_query.message.answer(text="Введите тип тренировки:")


@router.message(PlanState.training_type)
async def set_training_type(message: Message, state: FSMContext):
    await state.update_data(training_type=message.text)
    data = await state.get_data()
    print(data['time'])
    await set_training(message.from_user.id, data["date"], data["time"], data["training_type"])
    await message.answer("Тренировка успешно сохранена.")
    await state.clear()


@router.message(Command('view_plan'))
@router.message(F.text == "Посмотреть мои тренировки")
async def view_plan_command(message: Message):
    trainings = await get_trainings(message.from_user.id)
    answer = text_with_trainings(trainings)
    if trainings:
        await message.answer(text=f"Ваши запланированные тренировки:\n{answer}")
    else:
        await message.answer(text=f"У вас еще нет тренировок. Начинайте скорее, 100 килограмм сами себя не пожмут!")


@router.message(Command("get_advice"))
@router.message(F.text == "Получить совет от тренера")
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
