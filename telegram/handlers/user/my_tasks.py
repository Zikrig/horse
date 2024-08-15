from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import html

from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery

from os import getcwd
from datetime import datetime, timedelta

from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback

from config import *
from telegram.keyboards.simple_row import *
from telegram.handlers.not_handler_stuff import *

import table.work_with_database.task_work as tw
import table.work_with_database.admin_work as aw
from misc import send_notification

from telegram.states_work.time_changer import *
router = Router()

@router.message(F.text.lower() == 'мои поездки')  
async def get_tasks(message: Message, state: FSMContext):    
    await state.set_state(MyTasks.selectTasks)
    tasks = tw.select_dates_onready(mysqldata, message.from_user.id)
    tklav_raw = [[tasks[n][1].strftime("%d"), tasks[n][1].strftime("%m")]  for n in range(len(tasks))]

    tklav_raw = [date_to_str(tasks[n][1]) for n in range(len(tasks))]
    tklav = [f"{tk+1}. {'✅' if tasks[tk][2] else ''} {tklav_raw[tk]}" for tk in range(len(tklav_raw))] 

    ids = [tt[0]  for tt in tasks]
    
    await state.update_data(tasks_ids=ids)

    await message.answer(
        text = 'Выберите нужную поездку',
        reply_markup = make_row_keyboard(tklav + ['❌'])
    )

@router.message(MyTasks.selectTasks, F.text != '❌')
async def get_task(message: Message, state: FSMContext):    
    data =  await state.get_data()
    ids = data['tasks_ids']
    select_raw = int(message.text.split('.')[0]) - 1
    id_for = ids[select_raw]
    await state.update_data(task_id=id_for)
    await state.set_state(MyTasks.task)

    task_from_date = tw.select_task_by_id(mysqldata, id_for)
    wr = ':'.join(str(task_from_date[3]).split(':')[:2])
    if len(task_from_date) == 0:
        return 0
    if(not task_from_date[6] and not task_from_date[5]):
        await message.answer(
            text = f'''Активная заявка на поездку на {date_to_str(task_from_date[2])}.
Данное вами описание:
<i>{task_from_date[4]}</i>
Мы скоро с вами свяжемся.''',
            parse_mode='html',
            reply_markup = make_row_keyboard(['Изменить', 'Удалить', '❌'])
        )
    else:
        await message.answer(
            text = f'''Запланированная поездка на {date_to_str(task_from_date[2])}.
Начало поездки:
{wr}
''',
            parse_mode='html',
            reply_markup = make_row_keyboard(['Отменить', '❌'])
        )

@router.message(MyTasks.task, F.text == 'Удалить')
async def del_task(message: Message, state: FSMContext):    
    data =  await state.get_data()
    await state.set_state(MyTasks.zero)
    id = data['task_id']
    tw.delete_task_by_id(mysqldata, id)
    
    status = await actual_status(message.from_user.id, state)

    await message.answer(
        text = "Поездка успешно удалена",
        reply_markup = main_menu_global(status)
    )

@router.message(MyTasks.task, F.text == 'Отменить')
async def del_task(message: Message, state: FSMContext):    
    data =  await state.get_data()
    await state.set_state(MyTasks.zero)
    id = data['task_id']
    tw.cancel_task(mysqldata, id)
    
    status = await actual_status(message.from_user.id, state)

    await message.answer(
        text = "Поездка успешно отменена",
        reply_markup = main_menu_global(status)
    )
    
    for adm in aw.check_all_admin(mysqldata):
        task = tw.select_task_by_id(mysqldata, id)
        wr = ':'.join(str(task[3]).split(':')[:2])
        await send_notification(adm, f'<a href="tg://user?id={task[1]}">Пользователь</a> отменил поездку на {date_to_str(task[2])} на {wr}. Телефон: {task[3]}')


@router.message(MyTasks.task, F.text == 'Изменить')
async def alter_what(message: Message, state: FSMContext):  
    await state.set_state(MyTasks.alter)
    data =  await state.get_data()
    await message.answer(
        text = "Что именно вы хотите изменить в поездке?",
        reply_markup = make_row_keyboard(['Дата', 'Описание', '❌'])
    )

@router.message(MyTasks.alter, F.text == 'Дата')
async def alter_c(message: Message, state: FSMContext):  
    await state.set_state(MyTasks.alterDate)
    data =  await state.get_data()
    calendar = await SimpleCalendar(locale = 'ru_RU.UTF-8').start_calendar()
    await message.answer(
        text = 'Выберите новую дату.' + lc.holidays_pretty_hide(),
        reply_markup = calendar,
        parse_mode='html'
    )

@router.message(MyTasks.alter, F.text == 'Описание')
async def alter_d(message: Message, state: FSMContext):  
    await state.set_state(MyTasks.alterDescr)
    await message.answer(
        text = "Укажите новое описание",
        reply_markup = make_row_keyboard(['❌'])
    )

@router.message(MyTasks.alterDescr)
async def new_descr(message: Message,  state: FSMContext):
    data =  await state.get_data()
    id = data['task_id']
    tw.alt_task_descr(mysqldata, id, message.text.replace('\'', '"'))
    
    status = await actual_status(message.from_user.id, state)

    await state.set_state(MyTasks.zero)
    await message.answer(
            text = "Ваше новое описание сохранено",
            reply_markup = main_menu_global(status)
        )

@router.callback_query(SimpleCalendarCallback.filter(), MyTasks.alterDate)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,  state: FSMContext):
    status = await actual_status(callback_query.message.from_user.id, state)

    calendar = SimpleCalendar(
        locale='ru_RU.UTF-8'
    )
    calendar.set_dates_range(datetime(2024, 1, 1), datetime(2030, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    
    calendar = await SimpleCalendar(locale = 'ru_RU.UTF-8').start_calendar()
    if selected:
        if(date < datetime.today()):
            await callback_query.message.answer(
                text='Похоже, вы планируете поездку на прошедшее время. Пожалуйста, выберите дату в будущем)',
                reply_markup = calendar
            )
        elif(date-timedelta(days=60) > datetime.today()):
            await callback_query.message.answer(
                text='Похоже, вы планируете поездку более чем на два месяца вперед. Укажите пожалуйста более близкую дату.',
                reply_markup = calendar
            )
        elif(lc.is_day_holiday(date)):
            await callback_query.message.answer(
                text='Этот день - выходной. Пожалуйста, выберите другой',
                reply_markup = calendar
            )
        else:
            await callback_query.message.answer(
                f'''Вы выбрали дату {date_to_str(date)}. Теперь поездка запланирована на нее.''',
                reply_markup = main_menu_global(status)
            )
            await state.set_state(MyTasks.zero)
            data =  await state.get_data()
            id = data['task_id']
            tw.alt_task_date(mysqldata, id, date.strftime("%Y-%m-%d"))
