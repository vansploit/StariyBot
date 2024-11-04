import asyncio
from aiogram import Bot, Dispatcher

import config

from handlers import main_handler, admin_handler, user_handler

from plugins import p_message

import bot_logger
import db_bot
from keyboards.inline_kb import BotInlineKB

# Инициализация логгера и базы данных
logger = bot_logger.BotLogger().logger
BotBD = db_bot.MyDatabase(logger)

bot_ikb = BotInlineKB(logger)
p_message.logger = logger
 
# Функция для настройки обработчиков
def setup_handlers(bot, handlers):
    for handler in handlers:
        handler.BotDB = BotBD
        handler.sendel_msg = p_message.sendel_msg
        handler.bot_ikb = bot_ikb
        handler.bot = bot
        handler.logger = logger


# Запуск бота
async def main():
    bot = Bot(token = config.TOKEN)
    dp = Dispatcher()

    # Настройка обработчиков
    setup_handlers(
        bot,
        [admin_handler, main_handler, user_handler])

    dp.include_routers(
        main_handler.router,
        admin_handler.router,
        user_handler.router)

    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())