from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.filters import StateFilter
from aiogram.types import Message,FSInputFile, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from os import path
from datetime import datetime

from aiogram_calendar import SimpleCalendar, get_user_locale,  SimpleCalendarCallback

from telegram.keyboards.simple_row import *
from telegram.keyboards.inline_tasks import *

from telegram.handlers.not_handler_stuff import *
from table.work_with_database.task_work import *
from table.work_with_database.ban_work import *
from config import pgsdata, avas_dir
from telegram.states_work.time_changer import *

router = Router()

page_limiter = 5

@router.message(F.text == 'История')
async def default_mode(message: Message, state: FSMContext):
    await state.set_state(AdminTasks.tasksHistory)
    await message.answer(
        text = 'Историю за какую дату вы хотите посмотреть?',
        reply_markup = make_row_keyboard(['За дату', 'Вчера', 'За неделю', 'За месяц','Все', '❌'])
    )


@router.message(F.text == 'За дату', StateFilter(AdminTasks.tasksHistory))
async def alter_c(message: Message, state: FSMContext):  
    await state.set_state(AdminTasks.tasksHistory)
    calendar = await SimpleCalendar(locale = 'ru_RU.UTF-8').start_calendar()
    await message.answer(
        text = 'Выберите дату для проверки',
        reply_markup = calendar
    )

@router.message(StateFilter(AdminTasks.tasksHistory))
async def default_mode(message: Message, state: FSMContext):
    if message.text == 'Вчера':
        date_to_search = datetime.strftime(datetime.today() - timedelta(days=1), '%Y-%m-%d')
        prom_len = 1
    elif message.text == 'За неделю':
        date_to_search = datetime.strftime(datetime.today() - timedelta(days=7), '%Y-%m-%d')
        prom_len = 7
    elif message.text == 'За месяц':
        date_to_search = datetime.strftime(datetime.today()- timedelta(days=30), '%Y-%m-%d')
        prom_len = 30
    elif message.text == 'Все':
        date_to_search = datetime.strftime(datetime.today() - timedelta(days=360), '%Y-%m-%d')
        prom_len = 360
    else:
        await message.answer(
        text = 'Не понимаю, чего именно вы хотите.',
        )
        return True

    tasks = select_by_data_and_status(pgsdata, date_to_search, True, prom_len)

    if len(tasks) == 0:
        txt_res = 'Ни одной заявки не нашлось.'
    else:
        txt_res = 'Отлично. Какую же поездку вы ходите рассмотреть?'

    tasks_names = list(f'{t+1}. {tasks[t][0]}' for t in range(len(tasks)))
    await state.update_data(tasks=tasks)
    await state.update_data(tasks_names=tasks_names)
    await state.update_data(page_num=0)
    await message.answer(
        text = txt_res,
        reply_markup = tasks_inline(tasks_names, page_limiter).as_markup()
    )

@router.callback_query(F.data.startswith('blist'), StateFilter(AdminTasks.tasksHistory))
async def tasks_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page_num = data['page_num'] | 0

    tasks_names = data['tasks_names']
    tasks = data['tasks']
    butt_data = callback.data.replace('blist', '', 1)

    tasks_on_page_max = len(tasks_names)//page_limiter
    if len(tasks_names) % page_limiter != 0:
        tasks_on_page_max += 1
    
    if(butt_data == '<'):
        if page_num > 0:
            await state.update_data(page_num=page_num - 1)
            await callback.message.edit_reply_markup(reply_markup=tasks_inline(tasks_names, page_limiter, page_num - 1).as_markup())

    elif(butt_data == '>'):
        if page_num < tasks_on_page_max:
            await state.update_data(page_num=page_num + 1)
            await callback.message.edit_reply_markup(reply_markup=tasks_inline(tasks_names, page_limiter, page_num + 1).as_markup())
    else:
        task = tasks[int(butt_data) - 1]
        
        await state.update_data(user_to_work=task)

        name = task[0]
        user_id = task[1]
        phone = task[2]
        descr = task[3]
        photo_path = task[4]
        date_of = task[5]
        ride_descr = task[6]
        task_id = task[7]
        text_to_mes = f'''Поездка №{str(task_id)} от <b>{date_to_str(date_of)}</b>
От пользователя <a href="tg://user?id={user_id}"><b>{name}</b></a>
Связаться: {phone}
Описание пользователя:
<b><i>{descr}</i></b>
Особые условия поездки:
<b><i>{ride_descr}</i></b>'''
        
        photo_fin_path = avas_dir +'/'+ photo_path
        
        if path.isfile(photo_fin_path):
            await callback.message.answer_photo(
                photo=FSInputFile(photo_fin_path),
                caption=text_to_mes,
                parse_mode='html',
                )    
        else:
            await callback.message.answer(
                text=text_to_mes,
                parse_mode='html',
                ) 
    await callback.answer()
    await callback_inline_del(callback)
    return True

@router.callback_query(SimpleCalendarCallback.filter(), AdminTasks.tasksHistory)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,  state: FSMContext):
    calendar = SimpleCalendar(
        locale='ru_RU.UTF-8'
    )
    calendar.set_dates_range(datetime(2024, 1, 1), datetime(2030, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    
    calendar = await SimpleCalendar(locale = 'ru_RU.UTF-8').start_calendar()
    if selected:
        await callback_query.message.answer(
            f'''Вы выбрали дату {date_to_str(date)}. Проверяем наличие поездок''',
        )

    tasks = select_by_data_and_status(pgsdata, date.strftime("%Y-%m-%d"), True, 1)

    if len(tasks) == 0:
        txt_res = 'Ни одной заявки не нашлось.'
    else:
        txt_res = 'Отлично. Какую же заявку вы ходите рассмотреть?'

    tasks_names = list(f'{t+1}. {tasks[t][0]}' for t in range(len(tasks)))
    await state.update_data(tasks=tasks)
    await state.update_data(tasks_names=tasks_names)
    await state.update_data(page_num=0)
    await callback_query.message.answer(
        text = txt_res,
        reply_markup = tasks_inline(tasks_names, page_limiter).as_markup()
    )
