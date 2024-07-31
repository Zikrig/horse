from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import html

from aiogram.filters import StateFilter
from aiogram.types import Message,FSInputFile, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from os import getcwd, path
from datetime import datetime

from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback

from telegram.keyboards.simple_row import *
from telegram.keyboards.inline_tasks import *

from telegram.handlers.not_handler_stuff import *
from table.work_with_database.task_work import *
from table.work_with_database.ban_work import *
from config import pgsdata, avas_dir
from telegram.states_work.time_changer import *

from misc import send_notification

router = Router()

page_limiter = 5

@router.message(F.text == 'Поездки')
async def default_mode(message: Message, state: FSMContext):
    await state.set_state(AdminTasks.tasksGood)
    await message.answer(
        text = 'Вы в меню поездок. Какие поездки вас интересуют?',
        reply_markup = make_row_keyboard(['За дату', 'Сегодня', 'Завтра', 'Неделя', 'Месяц', 'Все', '❌'])
    )


@router.message(F.text == 'За дату', StateFilter(AdminTasks.tasksGood))
async def alter_c(message: Message, state: FSMContext):  
    await state.set_state(AdminTasks.tasksGood)
    calendar = await SimpleCalendar(locale = await get_user_locale(message.from_user)).start_calendar()
    await message.answer(
        text = 'Выберите дату для проверки',
        reply_markup = calendar
    )

@router.message(StateFilter(AdminTasks.tasksGood))
async def default_mode(message: Message, state: FSMContext):
    if message.text == 'Сегодня':
        date_to_search = datetime.strftime(datetime.today(), '%Y-%m-%d')
        prom_len = 1
    elif message.text == 'Завтра':
        date_to_search = datetime.strftime(datetime.today() + timedelta(days=1), '%Y-%m-%d')
        prom_len = 1
    elif message.text == 'Неделя':
        date_to_search = datetime.strftime(datetime.today(), '%Y-%m-%d')
        prom_len = 7
    elif message.text == 'Месяц':
        date_to_search = datetime.strftime(datetime.today(), '%Y-%m-%d')
        prom_len = 31
    elif message.text == 'Все':
        date_to_search = datetime.strftime(datetime.today(), '%Y-%m-%d')
        prom_len = 360
    else:
        await message.answer(
        text = 'Не понимаю, чего именно вы хотите.',
        )
        return True

    tasks = select_by_data_and_status(pgsdata, date_to_search, True, prom_len)

    if len(tasks) == 0:
        txt_res = f'Ни одной поездки за {date_to_search} не нашлось.'
    else:
        txt_res = 'Отлично. Какую же заявку вы ходите рассмотреть?'

    tasks_names = list(f'{t+1}. {tasks[t][0]}' for t in range(len(tasks)))
    await state.update_data(tasks=tasks)
    await state.update_data(tasks_names=tasks_names)
    await state.update_data(page_num=0)
    await message.answer(
        text = txt_res,
        reply_markup = tasks_inline(tasks_names, page_limiter).as_markup()
    )

@router.callback_query(F.data.startswith('blist'), StateFilter(AdminTasks.tasksGood))
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
        time_of = task[9]
        ride_descr = task[6]
        task_id = task[7]

        text_to_mes = f'''Запланированная поездка №{str(task_id)} от <b>{date_to_str(date_of)}</b>
От пользователя <b>{name}</b> на {str(time_of)} 
Связь: <b>{phone}</b>
<a href="tg://user?id={task[1]}">Телеграм юзера</a>
Описание пользователя:
<b><i>{descr}</i></b>
Особые условия поездки:
<b><i>{ride_descr}</i></b>'''
        
        photo_fin_path = avas_dir +'/'+ photo_path
        
        if check_ban(pgsdata, user_id) > 0:
            await callback.message.answer(
                text = f'Извините, пользователь {name} уже был забанен'
                )   
            return True
        
        if path.isfile(photo_fin_path):
            await callback.message.answer_photo(
                photo=FSInputFile(photo_fin_path),
                caption=text_to_mes,
                parse_mode='html',
                reply_markup=user_task_inline_to_cancel(user_id).as_markup()
                )    
        else:
            await callback.message.answer(
                text=text_to_mes,
                parse_mode='html',
                reply_markup=user_task_inline_to_cancel(user_id).as_markup()
                ) 
    await callback.answer()
    await callback_inline_del(callback)
    return True

@router.callback_query(F.data.startswith('cancel-'), StateFilter(AdminTasks.tasksGood))
async def tasks_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = data['user_to_work']
    await callback.answer()
    await callback.message.answer(
        text=f'Вы уверены, что хотите отменить поездку на {user[9]} за {user[5]} с пользователем {user[0]}?',
        reply_markup = really_cancel_inline(user[1]).as_markup()
    )
    await callback_inline_del(callback)

@router.callback_query(F.data.startswith('really-cancel-'), StateFilter(AdminTasks.tasksGood, AdminTasks.changeDate))
async def cancel_task_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = data['user_to_work']
    delete_task_by_id(pgsdata, user[7])
    await send_notification(user[1], f'Ваша поездка на {user[5]} {user[9]} была отменена')
    await callback.answer()
    await callback.message.edit_text(
        text=f'Поездка <a href="tg://user?id={user[1]}">пользователя</a>  на {user[5]} {user[9]} успешно отменена',
        parse_mode='html',
        reply_markup=None
        )

@router.callback_query(F.data.startswith('delete'), StateFilter(AdminTasks.tasksGood))
async def delete_callback(callback: CallbackQuery):
    await callback.message.delete()

@router.callback_query(F.data.startswith('change-time-'), StateFilter(AdminTasks.tasksGood, AdminTasks.changeDate))
async def change_time_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text='Выберите новое время для поездки',
        reply_markup=clocky().as_markup()
    )
    await callback_inline_del(callback)

@router.callback_query(F.data.startswith('alt-time-'), StateFilter(AdminTasks.tasksGood))
async def alt_time_callback(callback: CallbackQuery, state: FSMContext):
    str_time = callback.data.replace('alt-time-', '', 1)
    time = datetime.strptime(str_time, '%H:%M')
    data = await state.get_data()
    user = list(data['user_to_work'])
    print(user)
    user[9] = time
    print(user)
    await state.update_data(user_to_work=user)
    alt_task_time(pgsdata, user[7], str_time)
    await callback.answer()
    await callback.message.answer(f'Время поездки пользователя {user[0]} успешно изменено на {str_time}')
    await callback.message.delete()
    await send_notification(user[1], f'Время вашей поездки было изменено на {str_time}')
    await callback_inline_del(callback)

@router.callback_query(F.data.startswith('change-date-'), StateFilter(AdminTasks.tasksGood))
async def alt_date_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminTasks.changeDate)
    calendar = await SimpleCalendar(locale = 'ru_RU').start_calendar()
    await callback.message.answer(
        text = 'Выберите новую дату поездки',
        reply_markup = calendar
    )

@router.callback_query(SimpleCalendarCallback.filter(), AdminTasks.changeDate)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,  state: FSMContext):
    await state.set_state(AdminTasks.tasksGood)
    status = await actual_status(callback_query.message.from_user.id, state)

    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 1, 1), datetime(2030, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    
    calendar = await SimpleCalendar(locale = await get_user_locale(callback_query.from_user)).start_calendar()
    if selected:
        await callback_query.message.answer(
            f'''Новая дата поездки {date_to_str(date)}.''',
            # reply_markup = main_menu_global(status)
        )

        data = await state.get_data()
        user = data['user_to_work']
        alt_task_date(pgsdata, user[7], date)
        await callback_query.message.answer(f'Дата поездки пользователя {user[0]} успешно изменено на {date_to_str(date)}')
        await callback_query.message.delete()
        await send_notification(user[1], f'Дата вашей поездки была изменена на {date_to_str(date)}')
        await callback_inline_del(callback_query)


@router.callback_query(SimpleCalendarCallback.filter(), AdminTasks.tasksGood)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,  state: FSMContext):
    status = await actual_status(callback_query.message.from_user.id, state)

    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 1, 1), datetime(2030, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    
    calendar = await SimpleCalendar(locale = await get_user_locale(callback_query.from_user)).start_calendar()
    if selected:
        await callback_query.message.answer(
            f'''Вы выбрали дату {date_to_str(date)}. Проверяем наличие поездок''',
        )

    tasks = select_by_data_and_status(pgsdata, date.strftime("%Y-%m-%d"), False, 1)

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
