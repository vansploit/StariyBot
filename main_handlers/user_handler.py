from . import *

from states.User import AcceptOrderState, AddOrderState, EditOrdersState, EditAcceptedState

from text import user_formatter

from sub_handlers import r_add_order, r_accept_order, r_edit_orders, r_edit_accepted_orders

router = Router()
router.include_routers(r_add_order.router, r_edit_orders.router, r_accept_order.router, r_edit_accepted_orders.router)

#функция для построения меню страниц (orders для правильного отображения)
def get_navigation_menu(orders, user_id):
    user = BotDB.get_user(user_id)
    order = orders[0]
    answer = user_formatter.user_order(
                                order,
                                user['username'])
    stick = stickers.lst
    return user, order, answer, stick

@router.callback_query(F.data == "order_add")
async def add_order_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(alert_msg = None)
    await state.set_state(AddOrderState.wait)
    await sendel_msg(
                     call,
                     "Введите заказ через запятую и поставьте точку в конце",
                     bot_ikb.exit,
                     stickers.add)
    
    
@router.callback_query(F.data == "orders_list")
async def orders_list_handler(call: types.CallbackQuery, state: FSMContext):
    orders = BotDB.get_orders_by_user(call.from_user.id)
    if orders != None:
        user, order, answer, stick = get_navigation_menu(orders, call.from_user.id)
        menu = bot_ikb.get_orders_editor('start' if len(orders) > 1 else '')
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
    
    
@router.callback_query(F.data == "get_order")
async def accept_order_handler(call: types.CallbackQuery, state: FSMContext):
    orders = BotDB.get_not_picked_orders()
    if orders != None:
        user, order, answer, stick = get_navigation_menu(orders, call.from_user.id)
        menu = bot_ikb.get_accept_menu('start' if len(orders) > 1 else '')
        await state.update_data(
                        current_order_id = 0,
                        orders = orders,
                        order = order,
                        user = user)
        await state.set_state(AcceptOrderState.choose)
    else:
        answer = pre_texts.no_orders
        menu = bot_ikb.exit
        stick = stickers.no_exist
    await sendel_msg(call, answer, menu, stick)
    

@router.callback_query(StateFilter(
                        AcceptOrderState.ready,
                        AcceptOrderState.confirm),
                       F.data.in_({
                        "cancel",
                        "back"}))
async def accept_order_cancel_back(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await accept_order_handler(call, state)
    

@router.callback_query(F.data == "accepted_orders")
async def get_accepted_orders(call: types.CallbackQuery, state: FSMContext):
    orders = BotDB.get_picked_orders_by_user(call.from_user.id)
    if orders != None:
        user, order, answer, stick = get_navigation_menu(orders, call.from_user.id)
        menu = bot_ikb.get_accepted_menu('start' if len(orders) > 1 else '')
        await state.update_data(
                        current_order_id = 0,
                        orders = orders,
                        order = order,
                        user = user)
        await state.set_state(EditAcceptedState.choose)
    else:
        answer = pre_texts.no_orders
        menu = bot_ikb.exit
        stick = stickers.no_exist
    await sendel_msg(call, answer, menu, stick)
    
    
@router.callback_query(StateFilter(
                        EditAcceptedState.ready,
                        EditAcceptedState.throw,
                        EditAcceptedState.confirm),
                       F.data.in_({
                        "cancel",
                        "back"}))
async def accepted_order_cancel_back(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await get_accepted_orders(call, state)