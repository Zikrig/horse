from config import *
from table.work_with_database.db_init import *
# from table.init.db_init_use import *
from table.work_with_database.people_work import *
from table.work_with_database.task_work import *
from table.work_with_database.ban_work import *
from table.work_with_database.admin_work import *

# init_all(mysqldata)
# put_admin(mysqldata, 184374602)
# init_people_table(mysqldata)
# init_task_table(mysqldata)
# del_all(mysqldata)

# person_data = (1000, 'name', 'phone', 'description', 'photo')
# person_data2 = (1005, 'name', 'phone', 'description', 'photo')
# person_data3 = (1002, 'name', 'phone', 'description', 'photo')
# put_person(mysqldata, person_data)

# tg_person, date_of, time_of, descr_client, ready
# task_data = ('1000', '2024-01-08', '04:05', 'description', 'False')
# task_data2 = ('999', '2024-07-29', '04:05', 'description', 'False')
# person_data3 = (1002, 'name', 'phone', 'description', 'photo')
# put_task(mysqldata, task_data2)
# put_task(mysqldata, task_data)
print(select_all_tasks(mysqldata))

# person_gen(mysqldata, person_data)
# person_gen(mysqldata, person_data2)
# person_gen(mysqldata, person_data3)
# print(select_all_person(mysqldata))
# print(select_person(mysqldata, '184374602')) 
# print(select_unready_tasks(mysqldata, '1001'))
# print(select_dates_onready(mysqldata, '1001'))

# init_banned_table(mysqldata)
# print(select_person(mysqldata, 184374602))
# del_person(mysqldata, 184374602)
# delete_admin(mysqldata, 184374602)
# print(select_person(mysqldata, 184374602))
# del_person(mysqldata, 184374602)
# print(select_person(mysqldata, 184374602))
# put_banned(mysqldata, 1000)
# delete_ban(mysqldata, 184374602)
# print(check_ban(mysqldata, 1000))
# delete_task_by_user_id(mysqldata, 184374602)
# print(check_all_ban(mysqldata))

# print(*select_all_tasks(mysqldata))
# print(select_by_data_and_status(mysqldata, '2024-07-28', 'True'))
# r = select_by_data_and_status(mysqldata, '2024-07-30', 'False')
# print(r[0][4])
# print(select_hot_tasks(mysqldata))


# zap = 'CREATE TABLE admin(id SERIAL PRIMARY KEY, tg_person INT);'
# zap = 'SELECT * FROM admin;'
# send_some_mysql(mysqldata, zap)
