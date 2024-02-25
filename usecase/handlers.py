from aiogram.filters import CommandStart,Command,StateFilter
from aiogram.types import Message
from aiogram import Dispatcher, Router, F,types
from aiogram.fsm.context import FSMContext
from models.db import DB
from models.state import States
from models.kb import gender_select

dp = Dispatcher()
router = Router()


@dp.message(CommandStart())
async def start(msg: Message, state:FSMContext):
    if await DB.check_user(msg.from_user.id):
        await msg.answer(text=f"привет {msg.from_user.username}")
    else:
        await msg.answer(text="Привет, ты новичек так что давай зарегистрируемся")
        await msg.answer(text="Укажи свой пол", reply_markup=gender_select())
        await state.set_state(States.setgender)
@dp.callback_query(States.setgender, F.data.startswith("gender_"))
async def setgender(cb: types.CallbackQuery,state:FSMContext):
    data = cb.data
    _,gender = data.split("_")
    await state.update_data(gender=gender)
    await cb.message.answer("укажи свой возраст")
    await state.set_state(States.setage)
@dp.message(States.setage)
async def setage(msg:Message,state:FSMContext):
    try:
        age = int(msg.text)
    except ValueError:
        await msg.answer("призошла ошибка возраст указывайте цифрами")
        await msg.answer("укажи свой возраст")
        message = await dp.wait_for(types.Message, timeout=60)   #КОСТЫЛЬ
        await setage(msg,state)

    payload = await state.get_data()
    gender = payload["gender"]
    await DB.create_user(msg.from_user.id,age,gender)
    if gender == "male":
        gender = "мужской"
    else:
        gender = "женский"
    await msg.answer(f"Ваши данные успешно сохраненны.\nВозраст:{age}\nПол:{gender}")
    await state.clear()


@dp.message(StateFilter(None))
async def warning(msg:Message,state:FSMContext):
    await msg.answer("Чтобы начать напиши /start")
