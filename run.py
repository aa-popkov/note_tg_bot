import asyncio
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

from utils.bot import dp, bot
from utils.startup import on_startup
from handlers import router
from utils.scheduler import scheduler


async def main() -> None:
    scheduler.start()
    dp.startup.register(on_startup)
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    log_path = Path(__file__).parent.resolve() / "data" / "logs"
    if not log_path.exists():
        log_path.mkdir(parents=True)
    logging.basicConfig(
        format="{asctime} {filename} {levelname:8s} {message}",
        style="{",
        handlers=[
            RotatingFileHandler(
                "./data/logs/bot.log", maxBytes=10 * 1024, backupCount=5
            )
        ],
        level=logging.DEBUG,
    )
    asyncio.run(main())
