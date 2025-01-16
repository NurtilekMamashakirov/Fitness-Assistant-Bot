from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from app.database.db_requests import get_user


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        user = get_user(event.from_user.id)
        if user:
            result = await handler(event, data)
            return result
        else:
            await event.answer("Сначала зарегестрируйтесь.")
