from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.client import app
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user
from bot import logger

@app.on_message(filters.private & filters.command("start"))
async def welcome(client, message: Message):
    logger.info(f"Received /start from {message.from_user.id}")
    await message.reply("Bot is working!")

@app.on_message(filters.private & filters.command("info"))
# @verify_user(private=True)
async def user_info(client, message: Message):
    await message.reply(
        text=UserInfoText.format(sender=message.from_user)
    )

@app.on_message(filters.user(Telegram.OWNER_ID) & filters.command("log"))
async def send_log(client, message: Message):
    await message.reply_document("event-log.txt")
