from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message
from telegram.keyboards.simple_row import *
from telegram.handlers.not_handler_stuff import *
from telegram.states_work.status_state import *

router = Router()

@router.message(StateFilter(State()), F.text != '/start')
async def default_mode(message: Message, state: FSMContext):
    await state.set_state(SelectMode.user)
    status = await actual_status(message.from_user.id, state)
    if(status=='admin'):
        await message.answer(
        text = 'Бот был перезагружен, возвращаемся в главное меню',
        reply_markup = admin_menu()
    )
    else:
        await message.answer(
            text = 'Бот был перезагружен, возвращаемся в главное меню',
            reply_markup = main_menu_global(status)
        )
       
@router.message(F.text == '❌ Назад ❌', StateFilter(AlterAdmin, AdminTasks))
async def little_cancel(message: Message, state: FSMContext):
    await state.set_state(SelectMode.admin)
    await message.answer(
        text = 'Вы вернулись на главную.',
        reply_markup = admin_menu()
    )

@router.message(F.text =='❌ Назад ❌')
async def little_cancel_global(message: Message, state: FSMContext):
    await state.set_state(Reg.noth)
    status = await actual_status(message.from_user.id, state)
    # print(status)
    await message.answer(
        text = 'Вы вернулись на главную.',
        reply_markup = main_menu_global(status)
    )