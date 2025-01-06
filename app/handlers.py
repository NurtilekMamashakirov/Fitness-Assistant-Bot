from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.db_requests import set_user, get_user, update_aim, update_age, update_weight, update_height
from app.gigachat_utils import get_advice
from app.keybords import start_keyboard, sex_keyboard

router = Router()


class RegistrationState(StatesGroup):
    age = State()
    sex = State()
    weight = State()
    height = State()
    aim = State()


class UpdateState(StatesGroup):
    age = State()
    weight = State()
    height = State()
    aim = State()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=f"Добро пожаловать, {message.from_user.first_name}! \n"
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
    await state.update_data(age=message.text)
    await state.set_state(RegistrationState.sex)
    await message.answer(text="Укажите ваш пол:", reply_markup=sex_keyboard)


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
    await state.update_data(height=message.text)
    await state.set_state(RegistrationState.weight)
    await message.answer("Укажите ваш вес:")


@router.message(RegistrationState.weight)
async def registration_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await state.set_state(RegistrationState.aim)
    await message.answer(text="Укажите ваш опыт и цель тренировок (не более 800 символов):")


@router.message(RegistrationState.aim)
async def registration_aim(message: Message, state: FSMContext):
    await state.update_data(aim=message.text)
    data = await state.get_data()
    await set_user(tg_id=message.from_user.id, age=data["age"], sex=data["sex"], weight=data["weight"],
                   height=data["height"], aim=data["aim"])
    await message.answer("Регистариция успешно завершена!")


@router.message(F.text == "/set_aim")
async def set_aim_command(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await state.set_state(UpdateState.aim)
        await message.answer("Введите новую цель тренировок и не забудьте написать ваш текущий опыт.")


@router.message(UpdateState.aim)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(aim=message.text)
    data = await state.get_data()
    await update_aim(tg_id=message.from_user.id, aim=data["aim"])
    await message.answer("Цель успешно обновлена!")


@router.message(F.text == "/set_age")
async def set_aim_command(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await state.set_state(UpdateState.aim)
        await message.answer("Введите, сколько вам сейчас лет:")


@router.message(UpdateState.age)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await update_age(tg_id=message.from_user.id, age=data["age"])
    await message.answer("Возраст успешно обновлен!")


@router.message(F.text == "/set_weight")
async def set_aim_command(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await state.set_state(UpdateState.weight)
        await message.answer("Введите, сколько вы весите:")


@router.message(UpdateState.weight)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await update_weight(tg_id=message.from_user.id, weight=data["weight"])
    await message.answer("Вес успешно обновлен!")


@router.message(F.text == "/set_height")
async def set_aim_command(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await state.set_state(UpdateState.height)
        await message.answer("Введите, какой у вас рост:")


@router.message(UpdateState.height)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    data = await state.get_data()
    await update_height(tg_id=message.from_user.id, height=data["height"])
    await message.answer("Рост успешно обновлен!")


@router.message(F.text == "/my_info")
async def my_info(message: Message):
    user = await get_user(message.from_user.id)
    sex_decoder = {"male": "Мужской", "female": "Женский"}
    answer = f"Информация о вас: \n" \
             f"Возраст: {user.age}\nПол: {sex_decoder[user.sex]}\nРост: {user.height}\nВес: {user.weight}\nЦель и опыт: {user.aim}"
    await message.answer(answer)


@router.message(Command('/set_plan'))
async def set_plan_command(message: Message):
    # user describes his plan in informal text, program will use llm to parse this description, then save it in database
    pass


@router.message(Command('/view_plan'))
async def view_plan_command(message: Message):
    # bot will write all user's future trainings
    pass


@router.message(F.text == "/get_advice")
async def get_advice_command(message: Message):
    # at first bot will ask for a physical conditions of user
    # using llm program will return advised plan of training, plan will be depended from previous training, aim
    # and physical conditions
    advice = get_advice()
    await message.answer(advice)
