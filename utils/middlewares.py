import asyncio
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from aiogram.dispatcher.flags import get_flag


class LongTimeMiddleware(BaseMiddleware):
    clock_icons: list[str] = [
        "🕐",
        "🕑",
        "🕒",
        "🕓",
        "🕔",
        "🕕",
        "🕖",
        "🕗",
        "🕘",
        "🕙",
        "🕚",
        "🕛",
    ]
    msg = None

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        flag = get_flag(data, "long_operation")
        if not flag:
            return await handler(event, data)

        updated_task = asyncio.create_task(self.show_icon(event))
        result = await handler(event, data)
        await self.hide_icon()
        updated_task.cancel()
        return result

    async def show_icon(self, event: Message):
        index = 0
        self.msg = await event.bot.send_message(event.chat.id, self.clock_icons[index])
        while True:
            await asyncio.sleep(0.5)
            index = index + 1 if index < len(self.clock_icons) - 1 else 0
            icon = self.clock_icons[index]
            await event.bot.edit_message_text(
                icon, self.msg.chat.id, self.msg.message_id
            )

    async def hide_icon(self):
        await self.msg.bot.delete_message(self.msg.chat.id, self.msg.message_id)
