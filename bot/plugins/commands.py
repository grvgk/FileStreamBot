from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import app
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user

@app.on_message(filters.private & filters.command("start"))
@verify_user(private=True)
async def welcome(client, message: Message):
    await message.reply(
        text=WelcomeText % {'first_name': message.from_user.first_name},
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "ᴀᴅᴅ ᴛᴏ ᴄʜᴀɴɴᴇʟ", 
                url=f"https://t.me/{Telegram.BOT_USERNAME}?startchannel&admin=post_messages+edit_messages+delete_messages"
            )]
        ])
    )

@app.on_message(filters.private & filters.command("info"))
@verify_user(private=True)
async def user_info(client, message: Message):
    await message.reply(
        text=UserInfoText.format(sender=message.from_user)
    )

@app.on_message(filters.user(Telegram.OWNER_ID) & filters.command("log"))
async def send_log(client, message: Message):
    await message.reply_document("event-log.txt")
