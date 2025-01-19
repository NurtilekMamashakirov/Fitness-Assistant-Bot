from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from app.database.db_requests import set_user, get_user
from app.keybords import start_keyboard, sex_keyboard
from app.middlewares.logger_middleware import LoggerMiddleware
from app.utils import check_aim, check_age, check_height, check_weight

router = Router()
router.message.middleware(LoggerMiddleware())


class RegistrationState(StatesGroup):
    age = State()
    sex = State()
    weight = State()
    height = State()
    aim = State()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=f"Добро пожаловать! \n"
                              f"В нашем боты ты сможешь сделать свои тренировки более организованными и эффективными!\n"
                              f"Первым делом, зарегестрируйтесь.",
                         reply_markup=start_keyboard)


@router.callback_query(F.data == "registration")
async def registration_callback(callback: CallbackQuery, state: FSMContext):
    user = await get_user(tg_id=callback.from_user.id)
    if not user:
        await state.set_state(RegistrationState.age)
        await callback.message.answer(text="Введите ваш возраст:")
    if user:
        await callback.message.answer(text="Вы уже зарегестрированы!")


@router.message(RegistrationState.age)
async def registration_age(message: Message, state: FSMContext):
    if check_age(message.text):
        await state.update_data(age=message.text)
        await state.set_state(RegistrationState.sex)
        await message.answer(text="Укажите ваш пол:", reply_markup=sex_keyboard)
    else:
        await message.answer("Введенный возраст не корректен. Попробуйте заново.")


@router.callback_query(F.data == "man")
async def man_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sex="male")
    await state.set_state(RegistrationState.height)
    await callback.message.answer("Укажите ваш рост:")


@router.callback_query(F.data == "woman")
async def man_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sex="female")
    await state.set_state(RegistrationState.height)
    await callback.message.answer("Укажите ваш рост:")


@router.message(RegistrationState.height)
async def registration_height(message: Message, state: FSMContext):
    if check_height(message.text):
        await state.update_data(height=message.text)
        await state.set_state(RegistrationState.weight)
        await message.answer("Укажите ваш вес:")
    else:
        await message.answer("Введенный рост не корректен. Попробуйте заново.")


@router.message(RegistrationState.weight)
async def registration_weight(message: Message, state: FSMContext):
    if check_weight(message.text):
        await state.update_data(weight=message.text)
        await state.set_state(RegistrationState.aim)
        await message.answer(text="Укажите ваш опыт и цель тренировок (не более 800 символов):")
    else:
        await message.answer("Введенный вес не корректен. Попробуйте заново.")


@router.message(RegistrationState.aim)
async def registration_aim(message: Message, state: FSMContext):
    await state.update_data(aim=message.text)
    data = await state.get_data()
    if check_aim(message.text):
        await set_user(tg_id=message.from_user.id, age=data["age"], sex=data["sex"], weight=data["weight"],
                       height=data["height"], aim=data["aim"])
        await message.answer("Регистариция успешно завершена!")
        await state.clear()
    else:
        await message.answer(
            "Ваше сообщение не содержит информацию о цели тренировок или опыте. Попробуйте заново.")
