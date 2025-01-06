from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегестрироваться", callback_data="registration")],
    [InlineKeyboardButton(text="Список команд", callback_data="command list")]
])

sex_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мужчина", callback_data="man"),
     InlineKeyboardButton(text="Женщина", callback_data="woman")]
])
