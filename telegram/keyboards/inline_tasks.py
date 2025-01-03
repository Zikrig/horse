from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.states_work.time_changer import *

def tasks_inline(task_names, onpage=5, page_num = 0):
    builder = InlineKeyboardBuilder()
        
    for name_int in range(page_num*onpage, min((page_num+1)*onpage, len(task_names))):
        builder.row(InlineKeyboardButton(
            text = str(task_names[name_int]),
            callback_data = 'blist'+str(name_int + 1)
            ))
        
    if(len(task_names)>onpage):
        wer_on_last_chet = (page_num == len(task_names) // onpage-1) and len(task_names) % onpage == 0
        wer_on_last_nechet = (page_num == len(task_names) // onpage) and len(task_names) % onpage != 0
            
        if(page_num == 0):
            builder.row(InlineKeyboardButton(text = '>', callback_data = 'blist'+'>'))
        
        elif(wer_on_last_chet or wer_on_last_nechet):        
            builder.row(
                InlineKeyboardButton(text = '<', callback_data = 'blist'+'<')
                )
        else:
            builder.row(
                InlineKeyboardButton(text = '<', callback_data = 'blist'+'<'),
                InlineKeyboardButton(text = '>', callback_data = 'blist'+'>')
                )
    return builder

def user_task_inline(id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='⚠️', callback_data=f'ban-{id}'), 
        InlineKeyboardButton(text='✅', callback_data=f'approve-{id}')
        )
    return builder

def approve_inline(id, what_to_do):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Да', callback_data=f'really-{what_to_do}-{id}'), 
        InlineKeyboardButton(text='Отмена', callback_data=f'delete')
        )
    return builder

def clocky():
    builder = InlineKeyboardBuilder()
    for i in range(7, 24):
        builder.row(
            InlineKeyboardButton(text=f'{i}:00', callback_data=f'alt-time-{i}:00'), 
            InlineKeyboardButton(text=f'{i}:30', callback_data=f'alt-time-{i}:30') 
            )
    return builder

def user_task_inline_to_cancel(id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Отменить', callback_data=f'cancel-{id}'))
    builder.row(InlineKeyboardButton(text='изменить дату', callback_data=f'change-date-{id}'))
    builder.row(InlineKeyboardButton(text='изменить время', callback_data=f'change-time-{id}'))
    return builder

def really_cancel_inline(id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Да', callback_data=f'really-cancel-{id}'), 
        InlineKeyboardButton(text='Нет', callback_data=f'delete'))
    return builder

def holidays_all():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Дни недели', callback_data=f'weekdays'))
    builder.add(InlineKeyboardButton(text='Особые', callback_data=f'justdays'))
    return builder

def holidays_weekdays(lc):
    builder = InlineKeyboardBuilder()
    for day in range(len(lc.days)):
        builder.row(InlineKeyboardButton(text=("✅" if lc.weekdays[day] else "❌") + lc.days[day], callback_data=f'change-day-{day}'))
    builder.row(InlineKeyboardButton(text='❌ Назад ❌', callback_data=f'return-to-weeks'))
    return builder

def holidays_justdays(lc):
    builder = InlineKeyboardBuilder()
    for day in lc.get_justdays_list_for_90():
        builder.row(InlineKeyboardButton(text=date_to_str(day, False) + '❌', callback_data=f'del-justday-{day}'))
        
    builder.row(
        InlineKeyboardButton(text='Добавить', callback_data=f'add-justday'),
        InlineKeyboardButton(text='❌ Назад ❌', callback_data=f'return-to-weeks')
        )
    return builder
