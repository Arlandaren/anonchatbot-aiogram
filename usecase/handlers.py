from aiogram.filters import CommandStart,Command,StateFilter
from aiogram.types import Message
from aiogram import Dispatcher, Router, F,types,Bot
from aiogram.fsm.context import FSMContext
from models.db import DB
from models.state import States
from models.kb import *
from models.redis import *
import os
from typing import Union

bot = Bot(os.getenv("BOT_TOKEN"))

dp = Dispatcher()
router = Router()


@dp.message(CommandStart(), StateFilter(None))
async def start(msg: Message, state:FSMContext):
    if await DB.check_user(msg.from_user.id):
        await msg.answer(text=f"привет {msg.from_user.first_name}", reply_markup=main_menu())
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

@dp.message(F.text == "/search", StateFilter(None))
@dp.callback_query(F.data == "search_start", StateFilter(None))
async def search_start(query_or_message: Union[types.CallbackQuery, Message], state:FSMContext):
    await state.set_state(States.searching)
    msg = query_or_message
    id = query_or_message.from_user.id
    if isinstance(query_or_message, types.CallbackQuery):
        msg = query_or_message.message
    add_in_queue(id)
    await msg.answer("Идет поиск собеседника", reply_markup=search_menu())
    if check_queue():
        interlocutor = get_interlocutor(id)
        create_dialogue(id,interlocutor)
        text = "собеседник найден\n /stop для завершения диалога\n/next для поиска нового собеседника\n/link чтобы поделиться вашей ссылкой"
        await msg.answer(text)
        await bot.send_message(chat_id=interlocutor, text=text)
        await state.set_state(States.chating)
        await dp.fsm.get_context(bot, user_id=interlocutor, chat_id=interlocutor).set_state(States.chating)
        # await state.storage.set_state(key=StorageKey(cb.message.bot.id, chat_id=interlocutor, user_id=interlocutor), state=States.chating)


# @dp.message(F.text == "Остановить поиск",States.searching)
@dp.callback_query(F.data == "search_stop",States.searching)
async def search_stop(cb: types.CallbackQuery, state:FSMContext):
    await cb.message.answer(text="Поиск остановлен")
    del_from_queue(cb.from_user.id)
    await state.clear()
@dp.message(States.searching)
async def search_error(msg: Message):
    await msg.answer("Вы уже находитесь в поиске собеседника", reply_markup=search_menu())
@dp.message(States.chating, lambda m: m.text == "/stop")
async def stop_chating(msg: Message):
    interlocutor = find_dialogue(msg.from_user.id)
    await msg.answer(text="Диалог закончен")
    await bot.send_message(chat_id=interlocutor, text="Диалог закончен")
    del_dialogue(msg.from_user.id, interlocutor)
    await dp.fsm.get_context(bot, user_id=interlocutor, chat_id=interlocutor).clear()
    await dp.fsm.get_context(bot, user_id=msg.from_user.id, chat_id=msg.from_user.id).clear()
    
@dp.message(States.chating, F.text == "/next")
async def next_chatting(msg: Message, state: FSMContext):
    await stop_chating(msg)
    await state.set_state(States.searching)
    add_in_queue(msg.from_user.id)
    await msg.answer("Идет поиск собеседника", reply_markup=search_menu())
    if check_queue():
        interlocutor = get_interlocutor(msg.from_user.id)
        create_dialogue(msg.from_user.id,interlocutor)
        text = "собеседник найден\n /stop для завершения диалога\n/next для поиска нового собеседника\n/link чтобы поделиться вашей ссылкой"
        await msg.answer(text)
        await bot.send_message(chat_id=interlocutor, text=text)
        await state.set_state(States.chating)
        await dp.fsm.get_context(bot, user_id=interlocutor, chat_id=interlocutor).set_state(States.chating)
@dp.message(States.chating, F.text == "/link")
async def link_chating(msg: Message, state: FSMContext):
    interlocutor = find_dialogue(msg.from_user.id)
    await bot.send_message(chat_id=interlocutor, text=f"Внимание, собеседник отправил вам ссылку на свой профиль!!!\nhttps://t.me/{msg.from_user.username}")
    await msg.answer("Внимание, cобеседник получил ссылку на ваш профиль!!!")

@dp.message(States.chating, F.text)
async def chating(msg: Message):
    interlocutor = find_dialogue(msg.from_user.id)
    await bot.send_message(chat_id=interlocutor, text=msg.text)
@dp.message(States.chating, F.photo)
async def img_chating(msg: Message):
    interlocutor = find_dialogue(msg.from_user.id)
    await bot.send_photo(chat_id=interlocutor, photo=msg.photo[-1].file_id)
@dp.message(States.chating, F.sticker)
async def sticker_chating(msg:Message):
    interlocutor = find_dialogue(msg.from_user.id)
    await bot.send_sticker(chat_id=interlocutor, sticker=msg.sticker.file_id)
@dp.message(States.chating, F.voice)
async def voice_chating(msg: Message):
    interlocutor = find_dialogue(msg.from_user.id)
    await bot.send_voice(chat_id=interlocutor, voice=msg.voice.file_id)
@dp.message(States.chating, F.video)
async def video_chating(msg: Message):
    interlocutor = find_dialogue(msg.from_user.id)
    await bot.send_video(chat_id=interlocutor, video=msg.video.file_id)
@dp.message(States.chating)
async def error_chating(msg: Message):
    await msg.answer("❗ВНИМАНИЕ ❗\nНе поддерживаемый тип данных, сообщение не доставлено")
@dp.message(StateFilter(None))
async def warning(msg:Message,state:FSMContext):
    await msg.answer("У вас еще нет собеседника. Чтобы начать напиши /start или /search")
