from . import *

from states.User import EditAcceptedState

router = Router()

@router.callback_query(EditAcceptedState.choose, F.data.in_({"prev_page", "next_page"}))
async def navigate_accepted_orders(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    orders = state_data['orders']
    user = state_data['user']
    cur_ord_id = state_data['current_order_id']
    cur_ord_id, menu = (await navigate_orders(cur_ord_id, call.data, orders))
    
    if menu == None:
        return
    else:
        menu = bot_ikb.get_accepted_menu(menu)
    
    order = orders[cur_ord_id]
    await state.update_data(order = order)
    answer = user_formatter.user_order(order, user['username'])
    await state.update_data(current_order_id = cur_ord_id)
    await call.message.edit_text(answer, parse_mode="HTML", reply_markup=menu)
    
    
@router.callback_query(EditAcceptedState.choose, F.data == "order_ready")
async def order_get_ready(call: types.CallbackQuery, state: FSMContext):
    _id = (await state.get_data())['order']['id']
    await state.set_state(EditAcceptedState.ready)
    await sendel_msg(
                     call,
                     f"Вы подтверждаете выполнение заказа №{_id}?",
                     bot_ikb.confirm,
                     stickers.wait)
                     
@router.callback_query(EditAcceptedState.choose, F.data == "throw_order")
async def throw_order(call: types.CallbackQuery, state: FSMContext):
    _id = (await state.get_data())['order']['id']
    await state.set_state(EditAcceptedState.throw)
    await sendel_msg(
                     call,
                     f"Вы действительно отказываетесь от заказа №{_id}?",
                     bot_ikb.confirm,
                     stickers.wait)
                     
                     
@router.callback_query(EditAcceptedState.throw, F.data == "confirm")
async def throw_order_confirm(call: types.CallbackQuery, state: FSMContext):
    order = (await state.get_data())['order']
    _id = order['id']
    BotDB.update_order(_id, exec_id = None)
    await state.set_state(EditAcceptedState.confirm)
    await sendel_msg(
                     call,
                     f"Вы бросили заказ №{_id}",
                     bot_ikb.back,
                     stickers.confirm)
                     
    
@router.callback_query(EditAcceptedState.ready, F.data == "confirm")
async def order_get_ready_confirm(call: types.CallbackQuery, state: FSMContext):
    order = (await state.get_data())['order']
    _id = order['id']
    BotDB.finish_order(_id)
    await state.set_state(EditAcceptedState.confirm)
    await sendel_msg(
                     call,
                     f"Вы выполнили заказ №{_id}",
                     bot_ikb.back,
                     stickers.confirm)