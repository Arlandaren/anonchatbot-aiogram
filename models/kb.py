from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder

def gender_select():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="мужской",callback_data="gender_male")
    keyboard.button(text="женский",callback_data="gender_female")
    return keyboard.as_markup()

def main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="поиск",callback_data="search_start")
    keyboard.button(text="женский",callback_data="gender_female")
    return keyboard.as_markup()
def search_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="стоп", callback_data="search_stop")
    return keyboard.as_markup()