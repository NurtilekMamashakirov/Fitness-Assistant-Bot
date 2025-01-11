import time
from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.database.db_requests import set_user, get_user, update_aim, update_age, update_weight, update_height, \
    set_training, get_trainings
from app.utils import get_advice, check_aim, check_age, check_height, check_weight, text_with_trainings
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


class PlanState(StatesGroup):
    date = State()
    time = State()
    training_type = State()


class ConditionsState(StatesGroup):
    condition = State()


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
    if check_aim(data["aim"]) and check_age(data["age"]) and check_height(data["height"]) and check_weight(
            data["weight"]):
        await set_user(tg_id=message.from_user.id, age=data["age"], sex=data["sex"], weight=data["weight"],
                       height=data["height"], aim=data["aim"])
        await message.answer("Регистариция успешно завершена!")
    else:
        await message.answer("Один из полей заполнен некорректно, начните регистрацию заново.")
    await state.clear()


@router.message(Command("/set_aim"))
async def set_aim_command(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await state.set_state(UpdateState.aim)
        await message.answer("Введите новую цель тренировок и не забудьте написать ваш текущий опыт.")
    else:
        await message.answer("Первым делом зарегестрируйтесь!")


@router.message(UpdateState.aim)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(aim=message.text)
    data = await state.get_data()
    if check_aim(data["aim"]):
        await update_aim(tg_id=message.from_user.id, aim=data["aim"])
        await message.answer("Цель успешно обновлена!")
    else:
        await message.answer("Вы не описали цель или опыт. Попробуйте заново.")
    await state.clear()


@router.message(Command("set_age"))
async def set_aim_command(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await state.set_state(UpdateState.aim)
        await message.answer("Введите, сколько вам сейчас лет:")
    else:
        await message.answer("Первым делом зарегестрируйтесь!")


@router.message(UpdateState.age)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    if check_age(data["age"]):
        await update_age(tg_id=message.from_user.id, age=data["age"])
        await message.answer("Возраст успешно обновлен!")
    else:
        await message.answer("Введенный возраст не корректен. Попробуйте заново.")
    await state.clear()


@router.message(Command("set_weight"))
async def set_aim_command(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await state.set_state(UpdateState.weight)
        await message.answer("Введите, сколько вы весите:")
    else:
        await message.answer("Первым делом зарегестрируйтесь!")


@router.message(UpdateState.weight)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if check_weight(data["weight"]):
        await update_weight(tg_id=message.from_user.id, weight=data["weight"])
        await message.answer("Вес успешно обновлен!")
    else:
        await message.answer("Введенный вес не корректен. Попробуйте заново.")
    await state.clear()


@router.message(Command("set_height"))
async def set_aim_command(message: Message, state: FSMContext):
    if await get_user(message.from_user.id):
        await state.set_state(UpdateState.height)
        await message.answer("Введите, какой у вас рост:")
    else:
        await message.answer("Первым делом зарегестрируйтесь!")


@router.message(UpdateState.height)
async def set_aim(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    data = await state.get_data()
    if check_height(data["height"]):
        await update_height(tg_id=message.from_user.id, height=data["height"])
        await message.answer("Рост успешно обновлен!")
    else:
        await message.answer("Введенный рост не корректен. Попробуйте заново.")
    await state.clear()


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


@router.message(Command('set_plan'))
async def set_plan_command(message: Message, state: FSMContext):
    if get_user(message.from_user.id):
        await message.answer("Введите дату тренировки в формате день/месяц/год:")
        await state.set_state(PlanState.date)
    else:
        await message.answer("Первым делом зарегестрируйтесь!")


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
    await state.update_data(condition=message.text)
    data = await state.get_data()
    user = await get_user(message.from_user.id)
    trainings = await get_trainings(message.from_user.id)
    trainings_text = text_with_trainings(trainings)
    advice = get_advice(user.sex, user.age, user.height, user.weight, user.aim, data["condition"], trainings_text)
    await message.answer(advice)
