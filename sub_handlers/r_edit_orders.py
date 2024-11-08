from . import *

from states.User import EditOrdersState

router = Router()


@router.callback_query(EditOrdersState.choose, F.data.in_({"prev_page", "next_page"}))
async def page_navigate_orders(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    orders = state_data['orders']
    user = state_data['user']
    cur_ord_id = state_data['current_order_id']
    cur_ord_id, menu = (await navigate_orders(cur_ord_id, call.data, orders))
    
    if menu == None:
        return
    else:
        menu = bot_ikb.get_orders_editor(menu)
        
    order = orders[cur_ord_id]
    await state.update_data(order = order)
    answer = user_formatter.user_order(order, user.username)
    await state.update_data(current_order_id = cur_ord_id)
    await call.message.edit_text(answer, parse_mode="HTML", reply_markup=menu)
    
   
@router.callback_query(EditOrdersState.choose, F.data == "edit_order")
async def user_edit_order(call: types.CallbackQuery, state: FSMContext):
    answer = "Введите новый заказ и поставьте в конце точку"
    menu = bot_ikb.back
    stick = stickers.add
    await state.set_state(EditOrdersState.edit)
    await sendel_msg(call, answer, menu, stick)
    
    
@router.message(EditOrdersState.edit)
async def edit_order_input(msg: types.Message, state: FSMContext):
    clean_text = msg.text.replace(" ", "").replace(".", "")
    new_order = clean_text.lower().split(",")
    old_order = (await state.get_data())['order']
    await state.update_data(new_order = new_order)
    answer = f"Изменить заказ #{old_order.id}?\n"
    for i in old_order.order_list:
        answer += f" 🔹{i}\n"
    answer += " ⬇️⬇️⬇️⬇️⬇️\n"
    for i in new_order:
        answer += f" 🔹{i}\n"
    menu = bot_ikb.confirm
    stick = stickers.wait
    await state.set_state(EditOrdersState.confirm)
    await msg.delete()
    await sendel_msg(msg, answer, menu, stick)
    
    
@router.callback_query(EditOrdersState.confirm, F.data == "confirm")
async def edit_order_confirm(call: types.CallbackQuery, state: FSMContext):
    new_order = (await state.get_data())['new_order']
    old_order = (await state.get_data())['order']
    BotDB.update_order(old_order.id, order_list= new_order)
    answer = f"Заказ #{old_order.id} успешно изменен!"
    menu = bot_ikb.back
    stick = stickers.confirm
    await sendel_msg(call, answer, menu, stick)
    

@router.callback_query(EditOrdersState.choose, F.data == "delete_order")
async def user_del_order(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order = state_data['order']
    answer = f"Удалить заказ #{order.id}?"
    menu = bot_ikb.confirm
    stick = stickers.wait
    await state.set_state(EditOrdersState.delete)
    await sendel_msg(call, answer, menu, stick)
    
    
@router.callback_query(EditOrdersState.delete, F.data == "confirm")
async def u_del_order_confirm(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order = state_data['order']
    BotDB.delete_order(order.id)
    answer = "Заказ удалён!"
    menu = bot_ikb.back
    stick = stickers.confirm
    await sendel_msg(call, answer, menu, stick)