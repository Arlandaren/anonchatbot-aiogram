from aiogram import Bot
from usecase.handlers import bot
from usecase.handlers import dp,router
import os
import asyncio
from models.db import DB
from models.commands import my_commands
async def main():
    dp.include_routers(router)
    await DB.create()
    result: bool = await bot.set_my_commands(my_commands)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
