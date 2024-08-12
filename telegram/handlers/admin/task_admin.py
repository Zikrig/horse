from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from asyncio import sleep as asleep

from aiogram.filters import StateFilter
from aiogram.types import Message,FSInputFile, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from os import path
from datetime import datetime

from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback

from telegram.keyboards.simple_row import *
from telegram.keyboards.inline_tasks import *
from telegram.handlers.not_handler_stuff import *
from telegram.states_work.time_changer import *

from table.work_with_database.task_work import *
from table.work_with_database.ban_work import *
from config import mysqldata, avas_dir

from misc import send_notification

router = Router()

page_limiter = 5

@router.message(F.text == 'Заявки на поездки')
async def default_mode(message: Message, state: FSMContext):
    await state.set_state(AdminTasks.tasksRaw)
    await message.answer(
        text = 'Вы в меню неотвеченных заявок. Какие заявки вас интересуют?',
        reply_markup = make_row_keyboard(['За дату', 'Сегодня', 'Завтра', 'Неделя', 'Месяц', 'Все', '❌'])
    )

@router.message(F.text == 'За дату', StateFilter(AdminTasks.tasksRaw))
async def alter_c(message: Message, state: FSMContext):  
    await state.set_state(AdminTasks.tasksRaw)
    calendar = await SimpleCalendar(locale = 'ru_RU.UTF-8').start_calendar()
    await message.answer(
        text = 'Выберите дату для проверки',
        reply_markup = calendar
    )

@router.message(StateFilter(AdminTasks.tasksRaw))
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

    tasks = select_by_data_and_status(mysqldata, date_to_search, '0', prom_len)

    if len(tasks) == 0:
        txt_res = 'Ни одной заявки не нашлось.'
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

@router.callback_query(F.data.startswith('blist'), StateFilter(AdminTasks.tasksRaw))
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
        text_to_mes = f'''Запрос на поездку №{str(task_id)} от <b>{date_to_str(date_of)}</b>
От пользователя <a href="tg://user?id={task[1]}"><b>{name}</b></a>
Связаться: {phone}
Описание пользователя:
<b><i>{descr}</i></b>
Особые условия поездки:
<b><i>{ride_descr}</i></b>'''
        
        photo_fin_path = avas_dir +'/'+ photo_path
        
        if check_ban(mysqldata, user_id) > 0:
            await callback.message.answer(
                text = f'Извините, пользователь {name} уже был забанен'
                )   
            return True
        
        if path.isfile(photo_fin_path):
            await callback.message.answer_photo(
                photo=FSInputFile(photo_fin_path),
                caption=text_to_mes,
                parse_mode='html',
                reply_markup=user_task_inline(user_id).as_markup()
                )    
        else:
            await callback.message.answer(
                text=text_to_mes,
                parse_mode='html',
                reply_markup=user_task_inline(user_id).as_markup()
                ) 
    await callback.answer()
    await callback_inline_del(callback)
    return True

@router.callback_query(F.data.startswith('ban-'), StateFilter(AdminTasks.tasksRaw))
async def tasks_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # print(data)
    user = data['user_to_work']
    await callback.answer()
    if(check_ban(mysqldata, user[1])):
        await callback.message.answer(
        text=f'Пользователь {user[0]} уже был забанен.'
        )
        await callback.message.edit_reply_markup(None)
    elif(select_task_by_id(mysqldata, user[7])[5]):
        await callback.message.answer(
        text=f'Эта поездка уже была подтвержена'
        )
        await callback.message.edit_reply_markup(None)
    else:
        await callback.message.answer(
            text=f'Вы уверены, что хотите отправить пользователя {user[0]} в бан?',
            reply_markup = approve_inline(user[1], 'ban').as_markup()
        )
    await callback_inline_del(callback)

@router.callback_query(F.data.startswith('delete'), StateFilter(AdminTasks.tasksRaw))
async def delete_callback(callback: CallbackQuery):
    await callback.message.delete()

@router.callback_query(F.data.startswith('really-ban-'), StateFilter(AdminTasks.tasksRaw))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = data['user_to_work']
    put_banned(mysqldata, user[1])
    await callback.message.answer(f'Пользователь {user[0]} успешно добавлен в бан')
    await callback.message.delete()
    await callback_inline_del(callback)

@router.callback_query(F.data.startswith('approve-'), StateFilter(AdminTasks.tasksRaw))
async def tasks_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = data['user_to_work']
    await callback.answer()
    if(check_ban(mysqldata, user[1])):
        await callback.message.answer(
        text=f'Пользователь {user[0]} уже был забанен.'
        )
        await callback.message.edit_reply_markup(None)
    elif(select_task_by_id(mysqldata, user[7])[5]):
        await callback.message.answer(
        text=f'Эта поездка уже была подтвержена'
        )
        await callback.message.edit_reply_markup(None)
    else:
        await callback.message.answer(
            text=f'Пожалуйста, свяжитесь с пользователем {user[0]}. Подвердите поездку только если условия поездки обговорены.\nПодверить поездку?',
            reply_markup = approve_inline(user[1], 'approve').as_markup()
        )
    await callback_inline_del(callback)

@router.callback_query(F.data.startswith('really-approve-'), StateFilter(AdminTasks.tasksRaw))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=clocky().as_markup())

@router.callback_query(F.data.startswith('alt-time-'), StateFilter(AdminTasks.tasksRaw))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    str_time = callback.data.replace('alt-time-', '', 1)
    time = datetime.strptime(str_time, '%H:%M')
    data = await state.get_data()
    user = data['user_to_work']
    alt_task_time(mysqldata, user[7], time)
    await callback.answer()
    make_task_planned(mysqldata, user[7])
    await callback.message.answer(f'Поездка пользователя {user[0]} успешно подтверждена на время {str_time}')
    await callback.message.delete()
    await send_notification(user[1], f'Ваша поездка была успешно подтверждена на время {str_time}, {date_to_str(user[5])}')
    await callback_inline_del(callback)

@router.callback_query(SimpleCalendarCallback.filter(), AdminTasks.tasksRaw)
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

        tasks = select_by_data_and_status(mysqldata, date.strftime("%Y-%m-%d"), '0', 1)

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
