from . import *

from states.User import AcceptOrderState

router = Router()

@router.callback_query(AcceptOrderState.choose, F.data.in_({"prev_page", "next_page"}))
async def accept_navigate_orders(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    orders = state_data['orders']
    user = state_data['user']
    cur_ord_id = state_data['current_order_id']
    cur_ord_id, menu = (await navigate_orders(cur_ord_id, call.data, orders))
    
    if menu == None:
        return
    else:
        menu = bot_ikb.get_accept_menu(menu)
        
    order = orders[cur_ord_id]
    await state.update_data(order = order)
    answer = user_formatter.user_order(order, user['username'])
    await state.update_data(current_order_id = cur_ord_id)
    await call.message.edit_text(answer, parse_mode="HTML", reply_markup=menu)
    
@router.callback_query(AcceptOrderState.choose, F.data == "accept_order")
async def accept_order(call: types.CallbackQuery, state: FSMContext):
    order =(await state.get_data())['order']
    await state.set_state(AcceptOrderState.confirm)
    await sendel_msg(
                     call,
                     user_formatter.accept_order(order),
                     bot_ikb.confirm,
                     stickers.wait)
                     
                     
@router.callback_query(AcceptOrderState.confirm, F.data == "confirm")
async def confirm_accept_order(call: types.CallbackQuery, state: FSMContext):
    order = (await state.get_data())['order']
    BotDB.set_picked_order(order['id'], call.from_user.id)
    await state.set_state(AcceptOrderState.ready)
    await sendel_msg(
                     call,
                     f"Вы успешно приняли заказ №{order['id']}",
                     bot_ikb.back,
                     stickers.confirm)