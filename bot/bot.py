import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import Config, load_config
from config_data.set_menu import set_main_menu
from handlers import user_handlers, admin_handlers
from database.database import DataBase

load_dotenv()
logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(
                filename="main.log", mode="a", encoding="UTF-8"
                )
            ]
    )
    logger.info('Starting bot')
    config: Config = load_config()

    db: DataBase = DataBase()
    db.create_table_statistic()
    storage: MemoryStorage = MemoryStorage()
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)
    await set_main_menu(bot)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
