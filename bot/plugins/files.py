from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from secrets import token_hex
from bot import app
from bot.config import Telegram, Server
from bot.modules.decorators import verify_user
from bot.modules.telegram import send_message, filter_files
from bot.modules.static import *

@app.on_message(filters.private & filters.incoming & filters.create(filter_files))
@verify_user(private=True)
async def user_file_handler(client, message: Message):
    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)
    message.caption = f"`{secret_code}`"
    sent_msg = await send_message(message)
    message_id = sent_msg.id

    dl_link = f'{Server.BASE_URL}/dl/{message_id}?code={secret_code}'
    tg_link = f'{Server.BASE_URL}/file/{message_id}?code={secret_code}'
    deep_link = f'https://t.me/{Telegram.BOT_USERNAME}?start=file_{message_id}_{secret_code}'

    if (message.document and "video" in message.document.mime_type) or message.video:
        stream_link = f'{Server.BASE_URL}/stream/{message_id}?code={secret_code}'

        await message.reply(
            text=MediaLinksText % {
                'dl_link': dl_link,
                'tg_link': tg_link,
                'stream_link': stream_link
            },
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=dl_link),
                    InlineKeyboardButton("sᴛʀᴇᴀᴍ", url=stream_link)
                ],
                [
                    InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ", url=tg_link),
                    InlineKeyboardButton("ʀᴇᴠᴏᴋᴇ", callback_data=f"rm_{message_id}_{secret_code}")
                ]
            ])
        )
    else:
        await message.reply(
            text=FileLinksText % {
                'dl_link': dl_link,
                'tg_link': tg_link
            },
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=dl_link),
                    InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ", url=tg_link)
                ],
                [
                    InlineKeyboardButton("ʀᴇᴠᴏᴋᴇ", callback_data=f"rm_{message_id}_{secret_code}")
                ]
            ])
        )

@app.on_message(filters.channel & filters.create(filter_files) & ~filters.forwarded)
@verify_user()
async def channel_file_handler(client, message: Message):
    if message.caption and '#pass' in message.caption:
        return

    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)
    message.caption = f"`{secret_code}`"
    sent_msg = await send_message(message)
    message_id = sent_msg.id

    dl_link = f"{Server.BASE_URL}/dl/{message_id}?code={secret_code}"
    tg_link = f"{Server.BASE_URL}/file/{message_id}?code={secret_code}"

    if (message.document and "video" in message.document.mime_type) or message.video:
        stream_link = f"{Server.BASE_URL}/stream/{message_id}?code={secret_code}"

        try:
            await message.edit_caption(
                caption=f"`{secret_code}`",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=dl_link),
                        InlineKeyboardButton("sᴛʀᴇᴀᴍ", url=stream_link)
                    ],
                    [
                        InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ", url=tg_link)
                    ]
                ])
            )
        except Exception:
            pass
    else:
        try:
            await message.edit_caption(
                caption=f"`{secret_code}`",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=dl_link),
                        InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ", url=tg_link)
                    ]
                ])
            )
        except Exception:
            pass
