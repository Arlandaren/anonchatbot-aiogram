from aiogram import Bot
from usecase.router import dp,router
import os
import asyncio

async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp.include_routers(router)
    await dp.start_polling(bot)
asyncio.run(main())

