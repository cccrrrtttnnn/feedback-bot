import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher

from handlers.user import user
from handlers.admin import admin

from database.models import async_main

async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(user, admin)
    dp.startup.register(startup)
    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):
    await async_main()

if __name__  == '__main__':
    print('Бот включен!')
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print('Бот выключен!')