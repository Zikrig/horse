from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery

from datetime import datetime, timedelta

from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback

from config import *
from telegram.keyboards.simple_row import *

from telegram.handlers.not_handler_stuff import *
import table.work_with_database.task_work as tw
from table.work_with_database.admin_work import check_all_admin
from telegram.states_work.status_state import *
from telegram.states_work.time_changer import *

from misc import send_notification

router = Router()

@router.message(F.text.lower() == 'новая поездка')  
async def new_task(message: Message, state: FSMContext):    
    await state.set_state(NewTask.date)
    await message.answer(
        text = f'Выберите, когда желаете покататься!' + lc.holidays_pretty_hide(),
        reply_markup = make_row_keyboard(['Сегодня', 'Завтра', 'Другое', '❌ Назад ❌']),
        parse_mode='html'
    )

@router.message(F.text.in_(['Сегодня', 'Завтра']), NewTask.date)  
async def days(message: Message, state: FSMContext):    
    if(message.text == 'Сегодня'):
        # print(datetime.today())
        date = datetime.today()
    elif(message.text == 'Завтра'):
        date = datetime.today() + timedelta(days=1)
    
    if(lc.is_day_holiday(date)):
        await message.answer(
            text='Этот день - выходной. Пожалуйста, выберите другой'
        )
        return True
    await state.set_state(NewTask.descr)
    await state.update_data(date_of=date)
    await message.answer(
        f'''Вы выбрали дату {date_to_str(date)}. Теперь, пожалуйста, опишите особые обстоятельства поездки или нажмите "пропустить"
Например: \n "Мы будем всей семьей, два взрослых и два ребенка, опыт катания есть только у меня"\nили "Мне обязательно нужно успеть до 20:00, но можно перенести на завтра"''',
        reply_markup=make_row_keyboard(['Пропустить', '❌ Назад ❌'])
    )

@router.message(F.text.lower() == 'другое', NewTask.date)  
async def calend(message: Message, state: FSMContext):    
    await state.set_state(NewTask.dateCalendar)
    calendar = await SimpleCalendar(locale='ru_RU').start_calendar()
    await message.answer(
        text = 'Выберите, когда желаете покататься!',
        reply_markup = calendar
    )

@router.callback_query(SimpleCalendarCallback.filter(), NewTask.dateCalendar)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,  state: FSMContext):
    calendar = SimpleCalendar(
        locale='ru_RU'
    )
    calendar.set_dates_range(datetime(2024, 1, 1), datetime(2030, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    
    calendar = await SimpleCalendar(locale = 'ru_RU').start_calendar()
    if selected:
        if(date < datetime.today() - timedelta(days=1)):
            # print(date)
            # print(datetime.today())
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
            await state.update_data(date_of=datetime.strftime(date,"%Y-%m-%d"))
            await state.set_state(NewTask.descr)
            
            await callback_query.message.answer(
                f'''Вы выбрали дату {date_to_str(date)}. Теперь, пожалуйста, опишите особые обстоятельства поездки или нажмите "Пропустить".
Например: \n "Мы будем всей семьей, два взрослых и два ребенка, опыт катания есть только у меня"\nили "Мне обязательно нужно успеть до 20:00, но можно перенести на завтра"''',
                reply_markup=make_row_keyboard(['Пропустить', '❌ Назад ❌'])
            )

@router.message(NewTask.descr)  
async def descr(message: Message, state: FSMContext): 
    description = message.text.replace('\'', '"')
    if description == 'Пропустить':
        description = ''
    status = await actual_status(message.from_user.id, state)
    if(len(description) > 300):
        await message.answer(
            text = f'Длина вашего описания составила {len(description)} знаков! Пожалуйста, постарайтесь уложиться в 300 знаков.'
        )
    else:
        tasks = tw.select_unready_tasks(pgsdata, message.from_user.id)
        if(len(tasks) > 10): 
            await state.set_state('*')
            await message.answer(
                text = f'''Извините, вы не можете иметь более 10 заявок! Вы можете удалить или изменить те заявки, что у вас уже есть''',
                reply_markup = main_menu_global(status)
        )
        else:
            await state.set_state(NewTask.date)
            data = await state.get_data()
            # print(data['date_of'])
            # print(datetime.strftime(data['date_of'], '%Y-%m-%d'))
            # print(data['date_of'])
            
            date = datetime.strptime(data['date_of'], '%Y-%m-%d') if type(data['date_of']) == str else data['date_of']
            
            if description != '':
                dop = f' с текстом {description}'
            else:
                dop = '.'
            await message.answer(
                text = f'''Отлично, вы создали заявку! Мы постараемся перезвонить вам в ближайшее время.
Если не получится, мы попытаемся связаться в телеграме. Обязательно дождитесь обратной связи!
Если вы ошиблись в своей заявке или передумали, вы можете изменить или удалить ее в разделе "мои заявки".
Приятного катания!
Ваша заявка на {date_to_str(date)}{dop}''',
                reply_markup = main_menu_global(status)
            )

            task_data = [
                message.from_user.id,
                date,
                '00:00',
                description,
                False
            ]
            
            tw.put_task(pgsdata, task_data)
            for adm in check_all_admin(pgsdata):
                date_str = date_to_str(date.date())
                await send_notification(adm, f'<a href="tg://user?id={message.from_user.id}">Пользователь</a> хочет покататься {date_str}.\nПроверьте заявки!')
