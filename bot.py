import asyncio

from misc import dp, bot

from telegram.checker.check import check
from telegram.handlers.user import registration, stuff, task_user, my_tasks, get_horsehold_data
from telegram.handlers.admin import alter, menu_go, task_admin, task_ready, task_history, holidays

from telegram.middle.admin_middle import *
from telegram.middle.user_middle import *
from telegram.middle.baza_middle import *

from telegram.shedule.next_horseroute import check_time

async def main():
    for router_item in [alter, menu_go, task_admin, task_ready, task_history, holidays]:
        router_item.router.message.middleware(AdminMiddleware())

    for router_item in [task_user, my_tasks]:
        router_item.router.message.middleware(UserMiddleware())
        
    for router_item in [registration, get_horsehold_data]:
        router_item.router.message.middleware(BazaMiddleware())

    dp.include_routers(stuff.router, registration.router, task_user.router, my_tasks.router, get_horsehold_data.router)
    dp.include_routers(alter.router, menu_go.router, task_admin.router, task_ready.router, task_history.router, holidays.router)

    await dp.start_polling(bot)

async def checkercheck():
    # Корутина бота
    task = asyncio.create_task(main())
    asyncio.create_task(check_time())
    # while True:
    #     await asyncio.sleep(120)
    #     print('проспали еще 120 секунд')
    #     # Раз в пять секунд проверяем файл
    #     # Если там лежит 1 - останавливаем бота.
    #     if check():
    #         was_cancelled = task.result()
    #         print(was_cancelled)


if __name__ == "__main__":
    asyncio.run(main())