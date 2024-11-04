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
    
class AcceptOrderState(StatesGroup):
    choose = State()
    ready = State()
    confirm = State()
    
  
class EditAcceptedState(StatesGroup):
    choose = State()
    ready = State()
    throw = State()
    confirm = State()