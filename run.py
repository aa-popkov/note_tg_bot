import asyncio
import logging
import sys

from utils.bot import dp, bot
from utils.startup import on_startup
from handlers import router


async def main() -> None:
    dp.startup.register(on_startup)
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
