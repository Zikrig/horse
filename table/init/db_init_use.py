from table.work_with_database.db_init import *
from config import mysqldata

init_people_table(mysqldata)
init_task_table(mysqldata)
init_banned_table(mysqldata)
init_admin_table(mysqldata)
