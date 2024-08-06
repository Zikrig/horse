from aiogram.fsm.context import FSMContext

from config import mysqldata
from table.work_with_database import ban_work, people_work, admin_work

async def actual_status(id, state: FSMContext):
    user_data = await state.get_data()
    if not 'status' in user_data:
        st = get_new_status(mysqldata, id)
        await state.update_data(status=st)
        return st
    return user_data['status']

def get_new_status(mysqldata, id):
    pers = people_work.select_person(mysqldata, id)
    # print(pers)

    if len(pers) == 0:
        status = 'unreg'
        return status
    
    status = 'user'

    if ban_work.check_ban(mysqldata, id) != 0:
        # print(ban_work.check_ban(mysqldata, id))
        status = 'banned'
        return status

    if admin_work.check_admin(mysqldata, id) != 0:
        status = 'admin'
        return status
    
    return status

def reg_and_stat(mysqldata, person_data):
    people_work.person_gen(mysqldata, person_data)
    
    if admin_work.check_admin(mysqldata, person_data[0]) != 0:
        status = 'admin'
        return status
    
    return 'user'