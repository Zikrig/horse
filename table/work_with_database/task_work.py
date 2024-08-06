from datetime import datetime, timedelta

from table.work_with_database import conf_mysql as conf
def put_task(mysqldata, pd):
    return conf.send_some(mysqldata, f"INSERT INTO task(tg_person, date_of, time_of, descr_client, ready, canceled) VALUES ({pd[0]},'{pd[1]}','{pd[2]}','{pd[3]}','{pd[4]}',0)")

def alt_task(mysqldata, pd):
    return conf.send_some(mysqldata, f"UPDATE task SET (date_of, time_of, descr_client, ready) = ('{pd[1]}', '{pd[2]}', '{pd[3]}', '{pd[4]}') WHERE tg_person={str(pd[0])}")

def delete_task_by_id(mysqldata, id):
    return conf.send_some(mysqldata, f"DELETE FROM task WHERE id={str(id)}")

def delete_task_by_user_id(mysqldata, tg_id):
    return conf.send_some(mysqldata, f"DELETE FROM task WHERE tg_person={str(tg_id)}")

def alt_task_date(mysqldata, id, date):
    return conf.send_some(mysqldata, f"UPDATE task SET date_of='{date}' WHERE id={id}")

def alt_task_time(mysqldata, id, time):
    return conf.send_some(mysqldata, f"UPDATE task SET time_of='{time}' WHERE id={id}")

def alt_task_descr(mysqldata, id, descr):
    return conf.send_some(mysqldata, f"UPDATE task SET descr_client = '{descr}' WHERE id={id}")

def make_task_planned(mysqldata, id):
    return conf.send_some(mysqldata, f"UPDATE task SET ready = True WHERE id={id}")

def cancel_task(mysqldata, id):
    return conf.send_some(mysqldata, f"UPDATE task SET canceled = True WHERE id={id}")

def select_by_data_and_status(mysqldata, date_of, ready, daylen = 1):
    end_date = datetime.strftime(datetime.strptime(date_of, '%Y-%m-%d') + timedelta(days=daylen), '%Y-%m-%d')
    return conf.select_all(mysqldata, f'''SELECT people.name, people.tg_person, people.phone, people.description, people.photo, task.date_of, task.descr_client, task.id, task.canceled, task.time_of FROM task JOIN people ON people.tg_person=task.tg_person WHERE task.date_of>='{date_of}' AND task.date_of<'{end_date}' AND task.ready={str(ready)} AND task.canceled=0 AND NOT EXISTS (SELECT * FROM banned where banned.tg_person=people.tg_person) ORDER BY task.date_of, task.time_of''', False)
    
def select_task(mysqldata, tg_id):
    return conf.select_one(mysqldata, f"SELECT * FROM task WHERE tg_person={str(tg_id)}", False)

def select_all_tasks(mysqldata):
    return conf.select_all(mysqldata, f"SELECT * FROM task", False)

def select_unready_tasks(mysqldata, tg_id):
    return conf.select_one(mysqldata, f"SELECT COUNT(*) FROM task WHERE tg_person={str(tg_id)} AND DATE(date_of) >= CURRENT_DATE")
    
def select_dates_onready(mysqldata, tg_id):
    return conf.select_all(mysqldata, f"SELECT id, date_of, ready FROM task WHERE tg_person={str(tg_id)} AND DATE(date_of) >= CURRENT_DATE AND canceled=0", False)
    
def select_task_by_id(mysqldata, id):
    return conf.select_one(mysqldata, f"SELECT * FROM task WHERE id={str(id)}")

def select_hot_tasks(mysqldata):
    return conf.select_all(mysqldata, f"SELECT id FROM task WHERE DATE(date_of) = CURRENT_DATE AND canceled=0 AND ready=1 AND TIME(time_of) - interval 65 MINUTE < CURTIME() AND TIME(time_of) - interval 55 MINUTE > CURTIME()")