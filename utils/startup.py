from aiogram.types import BotCommand
from apscheduler.triggers.cron import CronTrigger

from config.config import config
from .bot import bot
from utils.scheduler import scheduler, hbd_notify


async def on_startup():
    commands = [
        BotCommand(command="/start", description="🏁 Старт"),
        BotCommand(command="/menu", description="🏠 Меню"),
        BotCommand(command="/notes", description="📝 Простые заметки"),
        BotCommand(command="/hbd", description="🥳 Дни рождения"),
        # BotCommand(command="/budget", description="💰 Бюджет"),
    ]
    await bot.set_my_commands(commands)

    for admin_id in config.TG_ADMIN_CHAT_ID:
        await bot.send_message(admin_id, "Бот перезапущен!", disable_notification=True)

    scheduler.add_job(
        func=hbd_notify,
        name="HBD Notification",
        id="global_hbd_notify",
        replace_existing=True,
        trigger=CronTrigger.from_crontab("0 9 */1 * *"),  # At 09:00 on every day-of-month
    )
