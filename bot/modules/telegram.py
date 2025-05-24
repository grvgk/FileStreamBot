from pyrogram.types import Message
from datetime import datetime
from mimetypes import guess_type
from bot import TelegramBot
from bot.config import Telegram
from bot.server.error import abort

async def get_message(message_id: int) -> Message | None:
    try:
        return await app.get_messages(chat_id=Telegram.CHANNEL_ID, message_ids=message_id)
    except Exception:
        return None

async def send_message(message: Message, send_to: int = Telegram.CHANNEL_ID) -> Message:
    return await app.send_message(chat_id=send_to, text=message.text or "", entities=message.entities)

def filter_files(update: Message):
    return bool(
        (
            update.document
            or update.photo
            or update.video
            or update.video_note
            or update.audio
            or update.animation
        )
        and not update.sticker
    )

def get_file_properties(message: Message):
    file = message.document or message.video or message.audio or message.voice or message.video_note or message.photo

    file_name = getattr(file, "file_name", None)
    file_size = getattr(file, "file_size", 0)
    mime_type = getattr(file, "mime_type", None)

    if not file_name:
        attributes = {
            'video': 'mp4',
            'audio': 'mp3',
            'voice': 'ogg',
            'photo': 'jpg',
            'video_note': 'mp4'
        }

        for attr, ext in attributes.items():
            if getattr(message, attr, None):
                file_type, file_format = attr, ext
                break
        else:
            abort(400, 'ɪɴᴠᴀʟɪᴅ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ.')

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'{file_type}-{date}.{file_format}'

    if not mime_type:
        mime_type = guess_type(file_name)[0] or 'application/octet-stream'

    return file_name, file_size, mime_type
