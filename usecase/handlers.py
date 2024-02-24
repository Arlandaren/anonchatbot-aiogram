from usecase.router import dp 
from aiogram.filters import CommandStart
from aiogram.types import Message

@dp.message(CommandStart())
async def start(msg: Message):
    msg.answer("привет")