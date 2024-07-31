from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters.callback_data import CallbackData
from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback

from datetime import datetime

from telegram.keyboards.simple_row import *
from telegram.keyboards.inline_tasks import *
from telegram.handlers.not_handler_stuff import *

from config import lc

router = Router()

@router.message(F.text == 'Выходные')
async def adm1(message: Message, state: FSMContext):
    await state.set_state(Holidays.menu)
    await message.answer(
        text = f'Выходные дни вашей конюшни: {lc.pretty_weekdays()}\nОсобые выходные в будущие три месяца:\n{lc.pretty_justdays()}',
        reply_markup = holidays_all().as_markup(),
        parse_mode='html'
    )

@router.callback_query(F.data.startswith('weekdays'))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=holidays_weekdays(lc).as_markup())

@router.callback_query(F.data.startswith('return-to-weeks'))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=holidays_all().as_markup())


@router.callback_query(F.data.startswith('change-day-'))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Holidays.menu)
    day = int(callback.data.replace('change-day-','', 1))
    lc.change_weekday(day)
    await callback.message.edit_text(
        text=f'Выходные дни вашей конюшни: {lc.pretty_weekdays()}\nОсобые выходные в будущие три месяца:\n{lc.pretty_justdays()}',
        parse_mode='html',
        reply_markup=holidays_weekdays(lc).as_markup())

@router.callback_query(F.data.startswith('justdays'))
async def delete_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Holidays.menu)
    await callback.message.edit_reply_markup(reply_markup=holidays_justdays(lc).as_markup())
 
@router.callback_query(F.data.startswith('del-justday-'))
async def delete_callback(callback: CallbackQuery):
    if lc.remove_from_justdays(callback.data.replace('del-justday-','', 1)):
        await callback.message.edit_text(
            text=f'Выходные дни вашей конюшни: {lc.pretty_weekdays()}\nОсобые выходные в будущие три месяца:\n{lc.pretty_justdays()}',
            parse_mode='html',
            reply_markup=holidays_justdays(lc).as_markup())
    

@router.callback_query(F.data.startswith('add-justday'))
async def make_calend(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Holidays.menu)
    calendar = await SimpleCalendar(locale = 'ru_RU').start_calendar()
    await callback.message.edit_reply_markup(reply_markup=calendar)


@router.callback_query(SimpleCalendarCallback.filter(), Holidays.menu)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,  state: FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 1, 1), datetime(2030, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    

    calendar = await SimpleCalendar(locale = await get_user_locale(callback_query.from_user)).start_calendar()
    if selected:
        lc.add_to_justdays(datetime.strftime(date,'%Y-%m-%d'))
        await callback_query.message.edit_text(
            text = f'Выходные дни вашей конюшни: {lc.pretty_weekdays()}\nОсобые выходные в будущие три месяца:\n{lc.pretty_justdays()}',
            reply_markup = holidays_justdays(lc).as_markup(),
            parse_mode='html'
        )