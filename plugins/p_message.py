from aiogram import types
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

logger = None

user_last_sticker = {}
user_last_message = {}

async def sendel_msg(msg, answer, menu = None, stick = None):
    del_msg, del_stick = None, None
    if type(msg) is types.CallbackQuery:
        call = msg
        msg = call.message
        if msg.chat.id not in user_last_message:
            await msg.delete()
    chat_id = msg.chat.id
    if chat_id in user_last_message:
        try:
            await user_last_message[chat_id].delete()
            await user_last_sticker[chat_id].delete()
        except TelegramBadRequest:
            logger.warning("Вызвано исключение TelegramBadRequest при удалении сообщения")
    if menu != None:
        if stick != None:
            del_stick = await msg.answer_sticker(stick)
        del_msg = await msg.answer(answer, reply_markup = menu, parse_mode = 'HTML')
    else:
        if stick != None:
            del_stick = await msg.answer_sticker(stick)
        del_msg = await msg.answer(answer, parse_mode = 'HTML')
    if del_msg != None:
        user_last_message[chat_id] = del_msg
    if del_stick != None:
        user_last_sticker[chat_id] = del_stick
    return del_msg