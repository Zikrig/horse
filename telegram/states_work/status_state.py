from aiogram.fsm.context import FSMContext

from config import pgsdata
from table.work_with_database import ban_work, people_work, admin_work

async def actual_status(id, state: FSMContext):
    user_data = await state.get_data()
    if not 'status' in user_data:
        st = get_new_status(pgsdata, id)
        await state.update_data(status=st)
        return st
    return user_data['status']

def get_new_status(pgsdata, id):
    pers = people_work.select_person(pgsdata, id)
    # print(pers)

    if len(pers) == 0:
        status = 'unreg'
        return status
    
    status = 'user'

    # print(ban_work.check_ban(pgsdata, id))
    if ban_work.check_ban(pgsdata, id) != 0:
        status = 'banned'
        return status
    cnt_adm = admin_work.check_admin(pgsdata, id)
    # print(cnt_adm)
    if cnt_adm != 0:
        status = 'admin'
        return status
    return status

def reg_and_stat(pgsdata, person_data):
    people_work.person_gen(pgsdata, person_data)
    
    if admin_work.check_admin(pgsdata, person_data[0]) != 0:
        status = 'admin'
        return status
    
    return 'user'