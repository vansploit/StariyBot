from . import *

from states.User import AddOrderState

router = Router()

async def delete_obj(*args):
    for i in args:
        if i != None:
            await i.delete()

@router.message(AddOrderState.wait ,F.text)
async def add_order_wait(msg: types.Message, state: FSMContext):
    
    alert_msg = (await state.get_data())['alert_msg'] 
    
    if msg.text.endswith("."):
        menu = None
        order = msg.text.lower().replace(".", "")
        order_lst = order.replace(" ", "").split(",")
        if len(order_lst) > 0:
            answer = user_formatter.add_ord(order_lst)
            menu = bot_ikb.confirm
            stick = stickers.wait
            await state.update_data(order = order_lst)
            await state.set_state(AddOrderState.confirm)
            await sendel_msg(msg, answer, menu)
            await delete_obj(msg, alert_msg)
            return
        else:
            stick = stickers.add_warn
            answer = "⚠️Список слишком короткий⚠️"
    else:
        stick = stickers.add_warn
        answer = "⚠️Поставь в конце точку (.)⚠️"
        
    await delete_obj(msg, alert_msg)
    alert_msg = await msg.answer(answer)
    await state.update_data(alert_msg = alert_msg)
    
@router.callback_query(AddOrderState.confirm, F.data == "confirm")
async def confirm_add_order(call: types.CallbackQuery, state: FSMContext):
    order = (await state.get_data())['order']
    BotDB.add_order(call.from_user.id, order)
    answer = "✅Заказ принят✅"
    menu = bot_ikb.exit
    await state.set_state(AddOrderState.finish)
    await sendel_msg(call, answer, menu, stickers.confirm)
    
@router.callback_query(AddOrderState.confirm, F.data == "cancel")
async def cancel_add_order(call: types.CallbackQuery, state: FSMContext):
    await add_order_handler(call, state)