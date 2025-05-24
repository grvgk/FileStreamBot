from pyrogram import filters
from pyrogram.types import CallbackQuery
from bot import app
from bot.modules.decorators import verify_user
from bot.modules.static import *
from bot.modules.telegram import get_message

@app.on_callback_query(filters.regex(r'^rm_'))
@verify_user(private=True)
async def delete_file(client, callback_query: CallbackQuery):
    query_data = callback_query.data.split('_')

    if len(query_data) != 3:
        return await callback_query.answer(InvalidQueryText, show_alert=True)

    message = await get_message(int(query_data[1]))

    if not message:
        return await callback_query.answer(MessageNotExist, show_alert=True)

    if query_data[2] != (message.text or message.caption):
        return await callback_query.answer(InvalidQueryText, show_alert=True)

    await message.delete()

    return await callback_query.answer(LinkRevokedText, show_alert=True)
