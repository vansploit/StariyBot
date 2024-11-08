import asyncio
from aiogram import Dispatcher

from config import bot
from main_handlers import main_handler, admin_handler, user_handler

from bot_logger import logger

logger.info("Бот запускается...")

# Запуск бота
async def main():
    
    
    dp = Dispatcher()

    dp.include_routers(
        main_handler.router,
        admin_handler.router,
        user_handler.router)

    await bot.delete_webhook(drop_pending_updates = True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)
    
    logger.info("Бот выключен!")


if __name__ == "__main__":
    asyncio.run(main())