from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class States(StatesGroup):
    setgender = State()
    setage = State()
    chating = State()
    searching = State()
# STATES = States()