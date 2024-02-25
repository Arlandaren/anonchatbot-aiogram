from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder

def gender_select():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="мужской",callback_data="gender_male")
    keyboard.button(text="женский",callback_data="gender_female")

    return keyboard.as_markup()