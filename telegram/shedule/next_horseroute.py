from asyncio import sleep as asleep
from datetime import datetime

from table.work_with_database.task_work import *
from misc import send_notification

from config import pgsdata

async def check_and_send():
    tasks = list(set(select_hot_tasks(pgsdata)))
    for task in tasks:
        task_info = select_task_by_id(pgsdata, task)
        tm = ':'.join(str(task_info[3]).split(':')[:2])
        await send_notification(task_info[1], f'Ваша поездка, запланированная на {tm}, будет менее, чем через час!')
    
async def check_time():
    while True:
        now = datetime.now()
        min_now = int(now.strftime("%M"))
        if min_now in [59, 29]:
            await check_and_send()
        await asleep(60)