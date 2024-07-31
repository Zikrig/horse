from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.keyboards.simple_row import *
from telegram.handlers.not_handler_stuff import *

router = Router()

@router.message(F.text == 'Админ-мод')
async def adm1(message: Message, state: FSMContext):
    await state.set_state(SelectMode.admin)
    await message.answer(
        text = 'Добро пожаловать в режим админа',
        reply_markup = admin_menu()
    )

@router.message(F.text == 'Юзер-мод')  
async def adm2(message: Message, state: FSMContext):      
    await state.set_state(SelectMode.user)

    status = await actual_status(message.from_user.id, state)

    await message.answer(
        text = 'Добро пожаловать в режим юзера',
        reply_markup = main_menu_global(status)
    )


