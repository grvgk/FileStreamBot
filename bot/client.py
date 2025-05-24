from pyrogram import Client
from bot.config import Telegram

app = Client(
    "bot",
    api_id=Telegram.API_ID,
    api_hash=Telegram.API_HASH,
    bot_token=Telegram.BOT_TOKEN
)
