from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from telegram.keyboards.simple_row import *
from telegram.states_work.status_state import *

class UserMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            message: types.Message,
            data: Dict[str, Any],
    ) -> Any:

        u_id = await self.get_id(message)
        
        status = get_new_status(pgsdata, u_id)
        
        if status == 'unreg':
            result = await message.answer(
            text = "Вы пока не зарегестрированы. Вам нужно пройти регистрацию",
            reply_markup = main_menu_global(status)
            )
            return result
        
        if status == 'banned':
            result = await message.answer(
            text = "К сожалению вы были заблокированы",
            reply_markup = ReplyKeyboardRemove()
            )
            return result
        
        if status in ['user', 'admin']:
            result = await handler(message, data)
        else:
            result = await message.answer(
            text = "Для выполнения этой команды нужны права админа, а у вас их нет.",
            reply_markup = main_menu_global(status)
            )
        return result
    
    async def get_id(self, msg: types.Message):
        return msg.from_user.id
    