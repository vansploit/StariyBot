from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from text import user_formatter, pre_texts, stickers

from db_bot import BotDB
from plugins.p_message import sendel_msg
from keyboards.inline_kb import bot_ikb
from bot_logger import logger

async def navigate_orders(cur_ord_id: int, action: str, orders: list) -> tuple:
    if action == "prev_page":
        if cur_ord_id - 1 >= 0:
            cur_ord_id -= 1
            menu = 'start' if cur_ord_id == 0 else 'middle'
        else:
            logger.error("Айди не может быть меньше 0")
            return cur_ord_id, None  # Возвращаем None для меню в случае ошибки
    elif action == "next_page":
        if cur_ord_id + 2 <= len(orders):
            cur_ord_id += 1
            menu = 'end' if cur_ord_id + 1 == len(orders) else 'middle'
        else:
            logger.error("Айди не может быть больше длины списка")
            return cur_ord_id, None  # Возвращаем None для меню в случае ошибки
    return cur_ord_id, menu