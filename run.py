import asyncio
import logging
import sys
from logging.handlers import RotatingFileHandler

from utils.bot import dp, bot
from utils.startup import on_startup
from handlers import router


async def main() -> None:
    dp.startup.register(on_startup)
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[RotatingFileHandler("./data/logs/bot.log", maxBytes=10*1024, backupCount=5)],
        level=logging.DEBUG,
    )
    asyncio.run(main())
