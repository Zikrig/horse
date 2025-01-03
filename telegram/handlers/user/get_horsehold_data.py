from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import html

from aiogram.types import Message,FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from telegram.keyboards.simple_row import *
from config import lc
from telegram.handlers.not_handler_stuff import *

router = Router()

@router.message(F.text == 'Конюшня')
async def phts(message: Message):
    if(len(lc.imgs)>0):
        album_builder = MediaGroupBuilder(
        caption=lc.description
        )
        for photo_id in lc.imgs:
            album_builder.add(
                type="photo",
                media=FSInputFile(photo_id)
            )

        await message.answer_media_group(
            media=album_builder.build(), 
            caption=lc.description,
            reply_markup = make_row_keyboard([
                '❌ Назад ❌'
            ])
        )
    else:
        await message.answer(
            text=lc.description,
            reply_markup = make_row_keyboard([
                '❌ Назад ❌'
            ])
        )
    if(not lc.coord1 is None):
        await message.answer_location(latitude=lc.coord1, longitude=lc.coord2)
