import psycopg2
from psycopg2 import Error

from datetime import datetime, timedelta
from table.work_with_database import conf
def put_task(pgsdata, pd):
    return conf.send_some(pgsdata, f"INSERT INTO task(tg_person, date_of, time_of, descr_client, ready, canceled) VALUES ('{pd[0]}','{pd[1]}','{pd[2]}','{pd[3]}','{pd[4]}',False)")

def alt_task(pgsdata, pd):
    return conf.send_some(pgsdata, f"UPDATE task SET (date_of, time_of, descr_client, ready) = ('{pd[1]}', '{pd[2]}', '{pd[3]}', '{pd[4]}') WHERE tg_person={str(pd[0])}")

def delete_task_by_id(pgsdata, id):
    return conf.send_some(pgsdata, f"DELETE FROM task WHERE id={str(id)}")

def delete_task_by_user_id(pgsdata, tg_id):
    return conf.send_some(pgsdata, f"DELETE FROM task WHERE tg_person={str(tg_id)}")

def alt_task_date(pgsdata, id, date):
    return conf.send_some(pgsdata, f"UPDATE task SET date_of='{date}' WHERE id={id}")

def alt_task_time(pgsdata, id, time):
    return conf.send_some(pgsdata, f"UPDATE task SET time_of='{time}' WHERE id={id}")

def alt_task_descr(pgsdata, id, descr):
    return conf.send_some(pgsdata, f"UPDATE task SET descr_client = '{descr}' WHERE id={id}")

def make_task_planned(pgsdata, id):
    return conf.send_some(pgsdata, f"UPDATE task SET ready = True WHERE id={id}")

def cancel_task(pgsdata, id):
    return conf.send_some(pgsdata, f"UPDATE task SET canceled = True WHERE id={id}")

def select_by_data_and_status(pgsdata, date_of, ready, daylen = 1):
    end_date = datetime.strftime(datetime.strptime(date_of, '%Y-%m-%d') + timedelta(days=daylen), '%Y-%m-%d')
    return conf.select_all(pgsdata, f'''SELECT people.name, people.tg_person, people.phone, people.describe, people.photo, task.date_of, task.descr_client, task.id, task.canceled, task.time_of FROM task JOIN people ON people.tg_person=task.tg_person WHERE task.date_of>='{date_of}' AND task.date_of<'{end_date}' AND task.ready={str(ready)} AND task.canceled=False AND NOT EXISTS (SELECT * FROM banned where banned.tg_person=people.tg_person) ORDER BY task.date_of, task.time_of''', False)
    
def select_task(pgsdata, tg_id):
    return conf.select_one(pgsdata, f"SELECT * FROM task WHERE tg_person={str(tg_id)}", False)

def select_all_tasks(pgsdata):
    return conf.select_all(pgsdata, f"SELECT * FROM task", False)

def select_unready_tasks(pgsdata, tg_id):
    return conf.select_one(pgsdata, f"SELECT COUNT(*) FROM task WHERE tg_person={str(tg_id)} AND date_of::date >= CURRENT_DATE")[0]
    
def select_dates_onready(pgsdata, tg_id):
    return conf.select_all(pgsdata, f"SELECT id, date_of, ready FROM task WHERE tg_person={str(tg_id)} AND date_of::date >= CURRENT_DATE AND canceled=False", False)
    
def select_task_by_id(pgsdata, id):
    return conf.select_one(pgsdata, f"SELECT * FROM task WHERE id={str(id)}")

def select_hot_tasks(pgsdata):
    return conf.select_all(pgsdata, f"SELECT id FROM task WHERE date_of::date = CURRENT_DATE AND canceled=False AND ready=True AND time_of::time - interval '65 minutes' < CURRENT_TIME AND time_of::time - interval '55 minutes' > CURRENT_TIME")