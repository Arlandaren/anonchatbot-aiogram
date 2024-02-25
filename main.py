from aiogram import Bot
from usecase.handlers import bot
from usecase.handlers import dp,router
import os
import asyncio
from models.db import DB

async def main():
    dp.include_routers(router)
    await DB.create()
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
