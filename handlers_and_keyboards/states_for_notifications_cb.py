from aiogram.fsm.state import StatesGroup, State


class SetNotifications(StatesGroup):
    time_zone = State()
    time_preferences = State()
