from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from asyncio import sleep as asleep

class SelectMode(StatesGroup):
    user = State()
    admin = State()

class Reg(StatesGroup):
    noth = State()
    name = State()
    phone = State()
    description = State()
    photo = State()

class UserAlt(StatesGroup):
    base = State()
    name = State()
    phone = State()
    description = State()
    photo = State()
    
class NewTask(StatesGroup):
    date = State()
    dateCalendar = State()
    descr = State()
    
class MyTasks(StatesGroup):
    selectTasks = State()
    task = State()
    alter = State()
    alterDate = State()
    alterDescr = State()
    zero = State()

class AlterAdmin(StatesGroup):
    alterGlobal = State()
    alterdescription = State()
    alterCoords = State()
    alterPhotos = State()
    addPhoto = State()

class AdminTasks(StatesGroup):
    tasksRaw = State()
    tasksGood = State()
    changeDate = State()
    tasksHistory = State()

class Holidays(StatesGroup):
    menu = State()


async def callback_inline_del(callback: CallbackQuery):
    await asleep(900)
    try:
        await callback.message.delete()
    except Exception as e:
        pass