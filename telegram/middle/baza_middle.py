
import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from telegram.keyboards.simple_row import *
from telegram.states_work.status_state import *

class BazaMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            message: types.Message,
            data: Dict[str, Any]
    ) -> Any:

        u_id = await self.get_id(message)
        
        status = get_new_status(pgsdata, u_id)
        
        if status == 'banned':
            result = await message.answer(
            text = "К сожалению вы были заблокированы",
            reply_markup = ReplyKeyboardRemove()
            )
            return result
       
        result = await handler(message, data)
        return result
    
    async def get_id(self, msg: types.Message):
        return msg.from_user.id
    