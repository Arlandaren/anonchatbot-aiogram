from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder

def gender_select():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="мужской",callback_data="gender_male")
    keyboard.button(text="женский",callback_data="gender_female")
    return keyboard.as_markup()

def main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="поиск",callback_data="search_start")
    return keyboard.as_markup()
def search_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Остановить поиск", callback_data="search_stop")
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)
def chating_menu():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Завершить диалог")
    keyboard.button(text="Поиск новго собеседника")
    keyboard.adjust(1)