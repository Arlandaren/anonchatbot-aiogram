from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class States(StatesGroup):
    setgender = State()
    setage = State()
# STATES = States()