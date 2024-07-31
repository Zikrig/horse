from table.work_with_database.db_init import *
from config import pgsdata

init_people_table(pgsdata)
init_task_table(pgsdata)
init_banned_table(pgsdata)
init_admin_table(pgsdata)
