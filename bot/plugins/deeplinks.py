from pyrogram import filters
from pyrogram.types import Message
from bot.client import app
from bot.modules.decorators import verify_user
from bot.modules.telegram import get_message, send_message
from bot.modules.static import *

@app.on_message(filters.private & filters.command("start"))
@verify_user(private=True)
async def send_file(client, message: Message):
    if not message.text.startswith("/start file_"):
        return

    payload = message.text.split()[-1].split('_')

    if len(payload) != 3:
        return await message.reply(InvalidPayloadText)

    original_msg = await get_message(int(payload[1]))

    if not original_msg:
        return await message.reply(MessageNotExist)

    if payload[2] != (original_msg.text or original_msg.caption):
        return await message.reply(InvalidPayloadText)

    # Clear text/caption to avoid duplication
    original_msg.text = ''
    original_msg.caption = ''

    await send_message(original_msg, send_to=message.chat.id)
