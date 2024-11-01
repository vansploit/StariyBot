from aiogram.fsm.state import State, StatesGroup

class AddOrderState(StatesGroup):
    wait = State()
    confirm = State()
    finish = State()
    
class EditOrdersState(StatesGroup):
    choose = State()
    edit = State()
    delete = State()
    confirm = State()