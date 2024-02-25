from aiogram import Bot
from usecase.handlers import dp,router
import os
import asyncio
from models.db import DB
async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp.include_routers(router)
    await DB.create()
    await dp.start_polling(bot)
    
asyncio.run(main())

