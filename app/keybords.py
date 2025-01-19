from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from app.utils import time2minutes, minutes2time

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегестрироваться", callback_data="registration")],
    [InlineKeyboardButton(text="Меню", callback_data="menu")]
])

sex_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мужчина", callback_data="man"),
     InlineKeyboardButton(text="Женщина", callback_data="woman")]
])

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text="Мой профиль", ), KeyboardButton(text="Получить совет от тренера")],
    [KeyboardButton(text="Запланировать тренировку"), KeyboardButton(text="Посмотреть мои тренировки")]
])


class TimeCallbackData(CallbackData, prefix="time"):
    value: str


def get_time_keyboard(date: datetime.date) -> InlineKeyboardMarkup:
    arg_keyboard = []
    buttons_in_row = 6
    hour_separation = 4
    if date > datetime.today():
        time = "00:00"
    else:
        time = datetime.now().strftime("%H:%M")
        minutes = time2minutes(time)
        time = minutes2time(minutes + (15 - minutes % 15))
    for i in range(24 * hour_separation // buttons_in_row):
        row = []
        for j in range(buttons_in_row):
            minutes_of_time = time2minutes(time)
            if minutes_of_time >= 60 * 24:
                break
            row.append(
                InlineKeyboardButton(text=time,
                                     callback_data=TimeCallbackData(value=time.replace(":", ";")).pack()))
            time = minutes2time(minutes_of_time + 60 // hour_separation)
        if len(row):
            arg_keyboard.append(row)

    return InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=arg_keyboard)
