from aiogram.types import BotCommand

from utils.config import config
from .bot import bot


async def on_startup():

    commands = [
        BotCommand(command="/start", description="🏁 Старт"),
        BotCommand(command="/menu", description="🏠 Меню"),
        BotCommand(command="/budget", description="💰 Бюджет"),
    ]
    await bot.set_my_commands(commands)
    for admin_id in config.TG_ADMIN_CHAT_ID:
        await bot.send_message(admin_id, "Бот перезапущен!", disable_notification=True)
