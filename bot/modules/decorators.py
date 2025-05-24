from pyrogram.types import Message, CallbackQuery
from typing import Callable, Union
from functools import wraps
from bot.config import Telegram

def verify_user(private: bool = False):
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(client, update: Union[Message, CallbackQuery]):
            # Check for private chat if required
            if private:
                if isinstance(update, Message) and update.chat.type != "private":
                    return
                if isinstance(update, CallbackQuery) and update.message.chat.type != "private":
                    return

            user_id = str(update.from_user.id)

            if not Telegram.ALLOWED_USER_IDS or user_id in Telegram.ALLOWED_USER_IDS:
                return await func(client, update)

        return wrapper
    return decorator
