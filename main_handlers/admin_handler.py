from . import *

from config import admins

from text import admin_formatter

router = Router()
router.message.filter(F.from_user.id.in_(set(admins)))

@router.message(Command("admin"))
async def message_with_text(msg: Message):
    answer = f"🛡️Админ панель @{msg.from_user.username}🛡️"
    await sendel_msg(msg, answer, bot_ikb.admin_panel)
    await msg.delete()
    
@router.callback_query(F.data=="a_orders")
async def adm_orders_list(call: types.CallbackQuery):
    user_id = call.from_user.id
    orders = BotDB.get_all_orders()
    answer = ""
    if len(orders) > 0:
        for order in orders:        
            username = BotDB.get_user(tg_id = order['tg_id'])['username']
            username = hlink(username, f'tg://user?id='+str(order['tg_id']))
            answer += f"📌Заказ #{order['id']}\n👤Пользователь {username}\n"
            for i in order['order_list'].split('/'):
                answer += f"    🔹{i}\n"
            answer += f"🗣️ Исполнитель {order['exec_id']}\n"
            answer += f"⏰{order['time']}\n\n"
    else:
        answer = pre_texts.no_orders
    await sendel_msg(call, answer, bot_ikb.exit)
    await call.answer()
    
@router.callback_query(F.data=="a_users")
async def adm_users_list(call: types.CallbackQuery):
    users = BotDB.get_all_users()
    answer = admin_formatter.user(users[0]) if len(users) > 0 else pre_texts.no_users
    menu = bot_ikb.admin_users
    await sendel_msg(call, answer, menu)
    await call.answer()