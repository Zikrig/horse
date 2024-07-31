from config import *
from table.work_with_database.db_init import *
from table.init.db_init_use import *
from table.work_with_database.people_work import *
from table.work_with_database.task_work import *
from table.work_with_database.ban_work import *
from table.work_with_database.admin_work import *

# init_all(pgsdata)
# init_people_table(pgsdata)
# init_task_table(pgsdata)

# person_data = (1000, 'name', 'phone', 'describe', 'photo')
# person_data2 = (1005, 'name', 'phone', 'describe', 'photo')
# person_data3 = (1002, 'name', 'phone', 'describe', 'photo')
# put_person(pgsdata, person_data)

# tg_person, date_of, time_of, descr_client, ready
# task_data = ('1000', '2024-01-08', '04:05', 'Describe', 'False')
# task_data2 = ('999', '2024-07-29', '04:05', 'Describe', 'False')
# person_data3 = (1002, 'name', 'phone', 'describe', 'photo')
# put_task(pgsdata, task_data2)
# put_task(pgsdata, task_data)
# print(select_all_tasks(pgsdata))

# person_gen(pgsdata, person_data)
# person_gen(pgsdata, person_data2)
# person_gen(pgsdata, person_data3)
# print(select_all_person(pgsdata))
# print(select_person(pgsdata, '184374602')) 
# print(select_unready_tasks(pgsdata, '1001'))
# print(select_dates_onready(pgsdata, '1001'))

# init_banned_table(pgsdata)
# print(select_person(pgsdata, 184374602))
# put_admin(pgsdata, 184374602)
# del_person(pgsdata, 184374602)
# delete_admin(pgsdata, 184374602)
# print(select_person(pgsdata, 184374602))
# del_person(pgsdata, 184374602)
# print(select_person(pgsdata, 184374602))
# put_banned(pgsdata, 1000)
# delete_ban(pgsdata, 189916381)
# print(check_ban(pgsdata, 1000))
# delete_task_by_user_id(pgsdata, 184374602)
# print(check_all_ban(pgsdata))

# print(*select_all_tasks(pgsdata))
# print(select_by_data_and_status(pgsdata, '2024-07-28', 'True'))
# r = select_by_data_and_status(pgsdata, '2024-07-30', 'False')
# print(r[0][4])
# print(select_hot_tasks(pgsdata))