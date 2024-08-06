from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from telegram.states_work.status_state import actual_status


def make_dobler_from_list(a:list):
    res = []
    add = []
    for f in range(len(a)):
        if f % 2 == 0:
            add = [a[f]]
        else:
            add.append(a[f])
            res.append(add)
            add = []
    if(len(a) % 2 == 1):
        res.append(add)
    # print(res)
    return res

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = make_dobler_from_list([KeyboardButton(text=item) for item in items])
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True)

def keyboard_proto(items: list[str]) -> ReplyKeyboardMarkup:
    if(len(items) <=2):
        row = [KeyboardButton(text=item) for item in items]
        return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True)
    
    rows = []
    for ii in range(len(items)//2 + 1):
        rows.append([KeyboardButton(text=item) for item in items[ii*2:ii*2+2]])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

def main_menu_admin():
    return make_row_keyboard([
                'Анкета',
                'Новая поездка',
                'Мои поездки',
                'Конюшня',
                'Админ-мод'
                ])

def main_menu_user():
    return make_row_keyboard([
                'Анкета',
                'Новая поездка',
                'Мои поездки',
                'Конюшня'
                ])

def main_menu_global(status):
    if status == 'admin':
        return main_menu_admin()
    if status == 'user':
        return main_menu_user()
    if status == 'unreg':
        return make_row_keyboard([
                'Регистрация',
                'Конюшня'
                ])

def admin_menu():
    return make_row_keyboard([
                'Изменить описание',
                'Заявки на поездки',
                'Поездки',
                'История',
                'Выходные',
                'Юзер-мод'
                ])

def alter_ancet():
    return make_row_keyboard(['Заполнить заново', 'Имя', 'Телефон', 'Описание', 'Фото', '❌'])