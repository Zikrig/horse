from datetime import datetime, timedelta
from table.work_with_database import conf_pgs as conf

def put_task(pgsdata, pd):
    return conf.send_some(
        pgsdata,
        f"INSERT INTO task(tg_person, date_of, time_of, descr_client, ready, canceled) VALUES ({pd[0]}, '{pd[1]}', '{pd[2]}', '{pd[3]}', {str(pd[4])}, 'False')"
    )

def alt_task(pgsdata, pd):
    return conf.send_some(
        pgsdata,
        f"UPDATE task SET date_of = '{pd[1]}', time_of = '{pd[2]}', descr_client = '{pd[3]}', ready = {str(pd[4])} WHERE tg_person = {pd[0]}"
    )

def delete_task_by_id(pgsdata, id):
    return conf.send_some(
        pgsdata,
        f"DELETE FROM task WHERE id = {id}"
    )

def delete_task_by_user_id(pgsdata, tg_id):
    return conf.send_some(
        pgsdata,
        f"DELETE FROM task WHERE tg_person = {tg_id}"
    )

def alt_task_date(pgsdata, id, date):
    return conf.send_some(
        pgsdata,
        f"UPDATE task SET date_of = '{date}' WHERE id = {id}"
    )

def alt_task_time(pgsdata, id, time):
    return conf.send_some(
        pgsdata,
        f"UPDATE task SET time_of = '{time}' WHERE id = {id}"
    )

def alt_task_descr(pgsdata, id, descr):
    return conf.send_some(
        pgsdata,
        f"UPDATE task SET descr_client = '{descr}' WHERE id = {id}"
    )

def make_task_planned(pgsdata, id):
    return conf.send_some(
        pgsdata,
        f"UPDATE task SET ready = 'True' WHERE id = {id}"
    )

def cancel_task(pgsdata, id):
    return conf.send_some(
        pgsdata,
        f"UPDATE task SET canceled = 'True' WHERE id = {id}"
    )

def select_by_data_and_status(pgsdata, date_of, ready, daylen=1):
    end_date = (datetime.strptime(date_of, '%Y-%m-%d') + timedelta(days=daylen)).strftime('%Y-%m-%d')
    zp = f'''
        SELECT 
            people.name, people.tg_person, people.phone, people.description, people.photo,
            task.date_of, task.descr_client, task.id, task.canceled, task.time_of 
        FROM task 
        JOIN people ON people.tg_person = task.tg_person 
        WHERE 
            task.date_of >= '{date_of}' 
            AND task.date_of < '{end_date}'
            AND task.ready = {str(ready)}
            AND task.canceled = 'False'
            AND NOT EXISTS (
                SELECT 1 FROM banned WHERE banned.tg_person = people.tg_person
            ) 
        ORDER BY task.date_of, task.time_of
        '''
    # print(zp)
    res = conf.select_all(
        pgsdata,
        zp
    )
    # print(res)
    return res

def select_task(pgsdata, tg_id):
    return conf.select_one(
        pgsdata,
        f"SELECT * FROM task WHERE tg_person = {tg_id}"
    )

def select_all_tasks(pgsdata):
    return conf.select_all(
        pgsdata,
        "SELECT * FROM task"
    )

def select_unready_tasks(pgsdata, tg_id):
    return conf.select_one(
        pgsdata,
        f'''
        SELECT COUNT(*) 
        FROM task 
        WHERE tg_person = {tg_id} AND date_of >= CURRENT_DATE
        '''
    )

def select_dates_onready(pgsdata, tg_id):
    return conf.select_all(
        pgsdata,
        f'''
        SELECT id, date_of, ready 
        FROM task 
        WHERE tg_person = {tg_id} AND date_of >= CURRENT_DATE AND canceled = 'False'
        '''
    )

def select_task_by_id(pgsdata, id):
    return conf.select_one(
        pgsdata,
        f"SELECT * FROM task WHERE id = {id}"
    )

def select_hot_tasks(pgsdata):
    return conf.select_all(
        pgsdata,
        '''
        SELECT id 
        FROM task 
        WHERE 
            date_of = CURRENT_DATE 
            AND canceled = 'False' 
            AND ready = 'True'
            AND time_of <= NOW() - INTERVAL '65 minutes' AND time_of > NOW() - INTERVAL '55 minutes'
        '''
    )
