from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from text import user_formatter, pre_texts, stickers

from db_bot import BotDB
from plugins.message import sendel_msg
from keyboards.inline_kb import bot_ikb
from bot_logger import logger