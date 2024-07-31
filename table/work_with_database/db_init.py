from table.work_with_database.conf import *

def init_people_table(pgsdata):
    send_some(pgsdata, "CREATE TABLE people (id SERIAL PRIMARY KEY, tg_person INT, name VARCHAR(50), phone VARCHAR(16), describe VARCHAR(300), photo VARCHAR(100))")

def init_task_table(pgsdata):
    send_some(pgsdata, "CREATE TABLE task(id SERIAL PRIMARY KEY, tg_person INT, date_of DATE, time_of TIME, descr_client VARCHAR(300), ready BOOL, canceled BOOL)")

def init_banned_table(pgsdata):
    send_some(pgsdata, "CREATE TABLE banned(id SERIAL PRIMARY KEY, tg_person INT)")

def init_admin_table(pgsdata):
    send_some(pgsdata, "CREATE TABLE admin(id SERIAL PRIMARY KEY, tg_person INT)")

def init_all(pgsdata):
    init_people_table(pgsdata)
    init_task_table(pgsdata)
    init_banned_table(pgsdata)
    init_admin_table(pgsdata)
