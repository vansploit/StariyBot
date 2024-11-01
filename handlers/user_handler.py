from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.User import AddOrderState, EditOrdersState
from text import user_formatter, pre_texts, stickers

BotDB = None
bot = None
sendel_msg = None
bot_ikb = None
logger = None

router = Router()

async def delete_obj(*args):
    for i in args:
        if i != None:
            await i.delete()

@router.callback_query(F.data == "order_add")
async def add_order_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(alert_msg = None)
    await sendel_msg(
                     call,
                     "Введите заказ через запятую и поставьте точку в конце",
                     bot_ikb.exit,
                     stickers.add)
    
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


@router.callback_query(F.data == "orders_list")
async def orders_list_handler(call: types.CallbackQuery, state: FSMContext):
    orders = BotDB.get_orders_by_user(call.from_user.id)
    if orders != None:
        user = BotDB.get_user(call.from_user.id)
        order = orders[0]
        answer = user_formatter.user_order(
                                order,
                                user['username'])
        menu = bot_ikb.get_orders_editor('start')
        stick = stickers.lst
        await state.update_data(
                        current_order_id = 0,
                        orders = orders,
                        order = order,
                        user = user)
        await state.set_state(EditOrdersState.choose)
    else:
        answer = pre_texts.no_orders
        menu = bot_ikb.exit
        stick = stickers.no_exist
    await sendel_msg(call, answer, menu, stick)
    
    
@router.callback_query(EditOrdersState.choose, F.data.in_({"prev_page", "next_page"}))
async def page_navigate_orders(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    orders = state_data['orders']
    user = state_data['user']
    cur_ord_id = state_data['current_order_id']
    match call.data:
        case "prev_page":
            if cur_ord_id-1 >= 0:
                cur_ord_id -= 1
                menu = bot_ikb.get_orders_editor(
                           'start' if cur_ord_id == 0 else 'middle')
            else:
                logger.error("Айди не может быть меньше 0")
                return
        case "next_page":
            if cur_ord_id+2 <= len(orders):
                cur_ord_id += 1
                menu = bot_ikb.get_orders_editor(
                           'end' if cur_ord_id+1 == len(orders) else 'middle')
            else:
                logger.error("Айди не может быть больше длины списка")
                return
    order = orders[cur_ord_id]
    await state.update_data(order = order)
    answer = user_formatter.user_order(order, user['username'])
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
    answer = f"Изменить заказ #{old_order['id']}?\n"
    for i in old_order['order_list']:
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
    BotDB.update_order(old_order['id'], order_list= new_order)
    answer = f"Заказ #{old_order['id']} успешно изменен!"
    menu = bot_ikb.back
    stick = stickers.confirm
    await sendel_msg(call, answer, menu, stick)
    

@router.callback_query(EditOrdersState.choose, F.data == "delete_order")
async def user_del_order(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order = state_data['order']
    answer = f"Удалить заказ #{order['id']}?"
    menu = bot_ikb.confirm
    stick = stickers.wait
    await state.set_state(EditOrdersState.delete)
    await sendel_msg(call, answer, menu, stick)
    
    
@router.callback_query(EditOrdersState.delete, F.data == "confirm")
async def u_del_order_confirm(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order = state_data['order']
    BotDB.delete_order(order['id'])
    answer = "Заказ удалён!"
    menu = bot_ikb.back
    stick = stickers.confirm
    await sendel_msg(call, answer, menu, stick)
    
    
@router.callback_query(StateFilter(
                        EditOrdersState.delete,
                        EditOrdersState.edit,
                        EditOrdersState.confirm),
                       F.data.in_({
                        "cancel",
                        "back"}))
async def edit_ord_cancel_back(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await orders_list_handler(call, state)
    