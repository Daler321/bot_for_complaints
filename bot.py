import asyncio
import logging
from aiogram import Bot, Dispatcher

from handlers.rgestration_handler import router as reg_router
from handlers.main_handler import router as main_router
from handlers.settings_handler import router as settings_router
from handlers.contact_handler import router as contact_router
from handlers.application_handler import router as application_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=<bot_token>)

dp = Dispatcher()

async def main():
    dp.include_routers(reg_router, main_router, settings_router, contact_router, application_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

send_message = bot.send_message