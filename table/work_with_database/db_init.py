from table.work_with_database.conf_mysql import *

def init_people_table(mysqldata):
    send_some(mysqldata, "CREATE TABLE people (id int NOT NULL AUTO_INCREMENT, tg_person INT NOT NULL, name VARCHAR(50), phone VARCHAR(16), description VARCHAR(300), photo VARCHAR(100), PRIMARY KEY (id))")

def init_task_table(mysqldata):
    send_some(mysqldata, "CREATE TABLE task(id int NOT NULL AUTO_INCREMENT, tg_person INT, date_of DATE, time_of TIME, descr_client VARCHAR(300), ready TINYINT(1), canceled TINYINT(1), PRIMARY KEY (id))")

def init_banned_table(mysqldata):
    send_some(mysqldata, "CREATE TABLE banned(id int NOT NULL AUTO_INCREMENT, tg_person INT, PRIMARY KEY (id))")

def init_admin_table(mysqldata):
    send_some(mysqldata, "CREATE TABLE admin(id int NOT NULL AUTO_INCREMENT, tg_person INT, PRIMARY KEY (id))")

def init_all(mysqldata):
    init_people_table(mysqldata)
    init_task_table(mysqldata)
    init_banned_table(mysqldata)
    init_admin_table(mysqldata)

def drop(mysqldata, tablename):
    send_some(mysqldata, f"DROP TABLE IF EXISTS {tablename};")

def del_all(mysqldata):
    drop(mysqldata, 'people')
    drop(mysqldata, 'task')
    drop(mysqldata, 'banned')
    drop(mysqldata, 'admin')