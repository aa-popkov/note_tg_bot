from aiogram.fsm.state import StatesGroup, State


class StartState(StatesGroup):
    start = State()
    start_register = State()
    cancel_register = State()


class MainState(StatesGroup):
    main = State()
    menu = State()
    notes = State()


class NotesState(StatesGroup):
    create_note = State()
    my_note = State()
    edit_note = State()
