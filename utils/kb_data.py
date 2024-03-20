from typing import NamedTuple


class StartRegister(NamedTuple):
    register: str = "🙋Начать регистрацию"
    cancel: str = "❌ Отмена"


class SendContact(NamedTuple):
    send: str = "📲 Отправить контакт"
    cancel: str = "❌ Отмена"


class MainMenu(NamedTuple):
    # account: str = "💰 Бюджет"
    # gym: str = "💪 GYM"
    notes: str = "📝 Заметки"
    cats: str = "🐈 Посмотреть котиков"
    hbd: str = "🥳 Дни рождения"


class NotesMenu(NamedTuple):
    make_note: str = "📋 Создать заметку"
    my_notes: str = "📑 Мои заметки"


class NoteEdit(NamedTuple):
    cancel: str = "❌ Отмена"


class CatsMenu(NamedTuple):
    give_cat: str = "🐱 Дай котика"
    back_to_menu: str = "🏠 Вернуться в главное меню"


class HbdMenu(NamedTuple):
    add_hbd: str = "➕ Добавить новый"
    show_in_msg: str = "💬 Посмотреть в сообщении"
    show_html: str = "📊 Посмотреть файлом"
    mange_hdb: str = "❌ Удалить"
    back_to_menu: str = "🏠 Вернуться в главное меню"
