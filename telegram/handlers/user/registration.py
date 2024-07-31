from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from telegram.keyboards.simple_row import *
from telegram.handlers.not_handler_stuff import *
from config import *
import table.work_with_database.people_work as pd
from telegram.states_work.status_state import *

router = Router()

@router.message(F.text =='Анкета')
async def little_cancel(message: Message, state: FSMContext):
    await state.set_state(Reg.noth)
    pers = pd.select_person(pgsdata, message.from_user.id)
    if len(pers) == 6:
        path_to_photo = f"{avas_dir}/{pers[5]}"
        capt = f'''Ваша анкета:
<b>Имя:</b>\t{pers[2]}
<b>Телефон:</b>\t{pers[3]}
<b>Описание:</b> \t{pers[4]}'''
        if(not os.path.exists(path_to_photo)):
            await message.answer(
                text = capt,
                parse_mode = 'html',
                reply_markup = make_row_keyboard([
                'Изменить анкету',
                '❌'
                ])
            )
        else:
            photo = FSInputFile(path=path_to_photo)
            await message.answer_photo(
                photo=photo,
                caption = capt,
                parse_mode = 'html',
                reply_markup = make_row_keyboard([
                'Изменить анкету',
                '❌'
                ])
            )
    else:
        await message.answer(
            text = "Мы пока не знакомы. Как насчет зарегистрироваться?",
            parse_mode = 'html',
            reply_markup = make_row_keyboard([
            'Изменить анкету',
            '❌'
            ])
            )
          
@router.message(F.text.in_(['/start','Заполнить заново', 'Регистрация']))
async def reg_start(message: Message, state: FSMContext):
    await state.set_state(SelectMode.user)
    await state.set_state(Reg.name)
    await message.answer(
        text = 'Как нам вас называть? Пожалуйста, введите свое имя',
        reply_markup = make_row_keyboard([
            '❌'
            ])
    )       

@router.message(Reg.name)  
async def reg_name(message: Message, state: FSMContext):
        if(len(message.text) < 4 or len(message.text) > 50):
            await message.answer(
                text = 'Нам нужно ваше имя, чтобы связаться с вами. Пожалуйста, укажите его. В имени должно быть от 4 до 50 знаков.',
            )
        else:
            # user_name = message.text
            await state.update_data(user_name=message.text)
            await state.set_state(Reg.phone)
            await message.answer(
                text = 'Спасибо! Теперь, пожалуйста, укажите ваш контактный телефон, чтобы мы вам перезвонили.',
                reply_markup = make_row_keyboard([
                '❌'
                ])
            )
            
@router.message(Reg.phone)  
async def reg_describe(message: Message, state: FSMContext):
    if(len(message.text) < 7 or len(message.text) > 15):
        await message.answer(
            text = "Это не похоже на номер телефона. Пожалуйста, введите номер, чтобы мы смогли с вами связаться.",
        )
    else:
        await state.update_data(user_phone=message.text)
        await state.set_state(Reg.describe)
        await message.answer(
            text = '''Нам нужно узнать о вас кое-что. Ответив на эти вопросы вы сильно сэкономите время телефонного разговора.
Или просто нажмите пропустить.\n
Сколько вам лет?
Сколько вы весите?
Какой у вас опыт катания?''',
            reply_markup = make_row_keyboard([
                'Пропустить',
                '❌',                    
                ])
            )
            
@router.message(Reg.describe)  
async def reg_describe(message: Message, state: FSMContext):
    if(len(message.text) > 300):
        await message.answer(
            text = f"Простите, но у вас целых {len(message.text)} символов, а ограничение - 300 символов.",
        )
    else:
        user_describe = message.text
        if user_describe == 'Пропустить':
            user_describe = ''
        await state.update_data(user_describe=user_describe)
        await state.set_state(Reg.photo)
        await message.answer(
            text = '''Пожалуйста, пришлите ваше фото или нажмите пропустить''',
            reply_markup = make_row_keyboard([
                'Пропустить',
                '❌'
                ])
            )
            
@router.message(Reg.photo)  
async def reg_describe(message: Message, state: FSMContext):
    user_id = message.from_user.id
    ava_name = f"ava_{user_id}.jpg"
    photo_path = f"{avas_dir}/{ava_name}"

    if(message.photo != '' and message.photo != None):
        await message.bot.download(
            message.photo[-1],
            destination=photo_path
            )
    data = await state.get_data()
    await state.set_state(Reg.noth)
    
    person_data = (user_id, data['user_name'], data['user_phone'], data['user_describe'], ava_name)
    status = reg_and_stat(pgsdata, person_data)
    await message.answer(
        text = '''Большое спасибо за заполнение анкеты!''',
        reply_markup = main_menu_global(status)
        )

@router.message(F.text == 'Изменить анкету', Reg.noth)  
async def alt_ance(message: Message, state: FSMContext):
    await state.set_state(UserAlt.base)
    await message.answer(
        text = 'Как вы хотите изменить анкету?',
        reply_markup = alter_ancet()
    )

@router.message(UserAlt.base)  
async def alt_user_base(message: Message, state: FSMContext):
    txt = message.text
    if(txt == 'Имя'):
        await state.set_state(UserAlt.name)
        await message.answer(
            text = 'Введите имя',
            reply_markup = make_row_keyboard(['❌'])
        )
    elif(txt == 'Телефон'):
        await state.set_state(UserAlt.phone)
        await message.answer(
            text = 'Введите новый телефон',
            reply_markup = make_row_keyboard(['❌'])
        )
    elif(txt == 'Описание'):
        await state.set_state(UserAlt.describe)
        await message.answer(
            text = '''Пожалуйста, введите новое описание. Ответив на эти вопросы вы сильно сэкономите время телефонного разговора.\n
Сколько вам лет?
Сколько вы весите?
Какой у вас опыт катания?''',
            reply_markup = make_row_keyboard(['❌'])
        )
    elif(txt == 'Фото'):
        await state.set_state(UserAlt.photo)
        await message.answer(
            text = 'Отправьте ваше новое фото',
            reply_markup = make_row_keyboard(['❌'])
        )
    else:
        await message.answer(
            text = 'Что-то не пойму, что вы имеете в виду'
        )

@router.message(UserAlt.name)
async def alt_name(message: Message, state: FSMContext):
    if message.text == '❌':
        return True
    if len(message.text) < 4 or len(message.text) > 50:
        await message.answer(
            text = 'Нам нужно ваше имя, чтобы связаться с вами. Пожалуйста, укажите его. В имени должно быть от 4 до 50 знаков.',
        )
    else:
        await message.answer(
            text = f'Имя успешно изменено на {message.text}'
        )
        pd.alt_person_field(pgsdata, message.from_user.id, 'name', message.text)
        await little_cancel(message, state)

@router.message(UserAlt.phone)
async def alt_phone(message: Message, state: FSMContext):
    if message.text == '❌':
        return True
    if len(message.text) < 7 or len(message.text) > 15:
        await message.answer(
            text = "Это не похоже на номер телефона. Пожалуйста, введите номер, чтобы мы смогли с вами связаться.",
        )
    else:
        await message.answer(
            text = f'Телефон успешно изменен на {message.text}'
        )
        pd.alt_person_field(pgsdata, message.from_user.id, 'phone', message.text)
        await little_cancel(message, state)

@router.message(UserAlt.describe)
async def alt_describe(message: Message, state: FSMContext):
    if message.text == '❌':
        return True
    if len(message.text) > 300:
        await message.answer(
            text = "Ваше описание длиннее 300 символов, пожалуйста, введите его чуть более сжато (вы можете скопировать ваше предыдущее сообщение).",
        )
    else:
        await message.answer(
            text = f'Описание успешно изменено на: \n<i>{message.text}</i>',
            parse_mose = 'html'
        )
        pd.alt_person_field(pgsdata, message.from_user.id, 'describe', message.text)
        await little_cancel(message, state)

@router.message(UserAlt.photo)
async def alt_photo(message: Message, state: FSMContext):
    if(message.photo == '' or message.photo == None):
        await message.answer(
            text = f"Вы не прислали фото. Пожалуста, пришлите фото",
        )
    else:
        user_id = message.from_user.id
        ava_name = f"ava_{user_id}.jpg"
        photo_path = f"{avas_dir}/{ava_name}"
        await message.bot.download(
            message.photo[-1],
            destination=photo_path
        )
        pd.alt_person_field(pgsdata, message.from_user.id, 'photo', ava_name)
        await message.answer(
            text = f'Фото успешно изменено.',
        )
        await little_cancel(message, state)