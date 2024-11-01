from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import admins
from text import stickers

BotDB = None
bot = None
sendel_msg = None
bot_ikb = None
logger = None

router = Router()

@router.message(StateFilter(None), Command("start"))
async def cmd_start(msg: Message):
    if BotDB.user_exists(msg.from_user.id) == False:
        BotDB.add_user(msg.from_user.id, msg.from_user.username, "admin" if msg.from_user.id in admins else "user")
    await sendel_msg(msg, f"@{msg.from_user.username}, приветствую в боте для заказов!", bot_ikb.start, stickers.hello)
    
@router.callback_query(F.data == "menu")
async def menu_callback(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await sendel_msg(call, f"@{call.from_user.username}, приветствую в боте для заказов!", bot_ikb.start, stickers.hello)