from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import html

from aiogram.types import Message,FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import StateFilter

from datetime import datetime

from telegram.keyboards.simple_row import *
from config import lc, horseh_dir

from telegram.handlers.not_handler_stuff import *

router = Router()

@router.message(F.text == 'Изменить описание',  StateFilter(SelectMode.admin, Holidays.menu))
async def admd1(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.alterGlobal)
    await message.answer(
        text = 'Вот как выглядит анкета прямо сейчас. Что именно вы хотите поменять или добавить?',
        reply_markup = make_row_keyboard([
            'Описание',
            'Координаты',
            'Фото',
            '❌ Назад ❌'
            ])
    )
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
        )
    else:
            await message.answer(
            text=lc.description,
        )
    if(not lc.coord1 is None):
        await message.answer_location(latitude=lc.coord1, longitude=lc.coord2)

@router.message(F.text == 'Описание', AlterAdmin.alterGlobal)
async def opis(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.alterdescription)
    await message.answer(
        text = 'Введите новое описание. Вы можете использовать функционал телеграма - курсив и прочее.',
        parse_mode='html',
        reply_markup = make_row_keyboard([
            '❌ Назад ❌'
            ])
    )

@router.message(AlterAdmin.alterdescription)
async def opis2(message: Message, state: FSMContext):
    await state.set_state(SelectMode.admin)
    lc.set_descr(message.html_text)
    await message.answer(
        text = 'Описание изменено!',
        parse_mode='html',
        reply_markup = admin_menu()
    )

@router.message(F.text == 'Координаты', AlterAdmin.alterGlobal)
async def opis3(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.alterCoords)
    await message.answer(
        text = 'Введите новые координаты на отдельных строках без посторонних симоволов, например:\n45.422\n25.44332',
        reply_markup = make_row_keyboard([
            '❌ Назад ❌'
            ])
    )

@router.message(AlterAdmin.alterCoords)
async def opis4(message: Message, state: FSMContext):
    await state.set_state(SelectMode.admin)
    res_coords = lc.set_coords(message.text)
    if res_coords:
        await message.answer(
            text = 'Координаты изменены!',
            reply_markup = admin_menu()
        )
    else:
        await message.answer(
            text='Какая-то проблема с координатами попробуйте еще раз.'
        )

@router.message(F.text == 'Фото', AlterAdmin.alterGlobal)
async def opis(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.alterPhotos)
    await message.answer(
        text = 'Вы можете удалить или добавить фото',
        parse_mode='html',
        reply_markup = make_row_keyboard([f"{i+1} ❌" for i in range(len(lc.imgs))]+['➕','❌'])
    )

@router.message(AlterAdmin.alterPhotos, F.text == '➕')
async def al(message: Message, state: FSMContext):
    await state.set_state(AlterAdmin.addPhoto)
    await message.answer(
        text = 'Отправьте новое фото',
        reply_markup = make_row_keyboard([f"{i+1} ❌" for i in range(len(lc.imgs))]+['➕','❌'])
    )

@router.message(AlterAdmin.addPhoto)
async def al(message: Message, state: FSMContext):
    if(message.photo == '' or message.photo == None):
        await message.answer(
            text = f"Вы не прислали фото. Пожалуйста, пришлите фото",
        )
    else:
        await state.set_state(AlterAdmin.alterPhotos)
        user_id = message.from_user.id
        horseh_name = f"horse_{user_id}_{str(datetime.now().time()).replace('.', '').replace(':', '')}.jpg"
        photo_path = f"{horseh_dir}/{horseh_name}"
        await message.bot.download(
        message.photo[-1],
        destination=photo_path
        )

    lc.add_photo_to_file(horseh_name)
    await message.answer(
        text = 'Большое спасибо добавление нового фото!',
        reply_markup = make_row_keyboard([f"{i+1} ❌" for i in range(len(lc.imgs))]+['➕','❌'])
    )

@router.message(AlterAdmin.alterPhotos)
async def al(message: Message, state: FSMContext):
    num, _ = message.text.split()
    lc.del_photo_by_num(int(num)-1)
    await message.answer(
        text = 'Фото успешно удалено',
        reply_markup = make_row_keyboard([f"{i+1}❌" for i in range(len(lc.imgs))]+['➕','❌'])
    )