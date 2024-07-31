import psycopg2
from psycopg2 import Error

from table.work_with_database import conf

def put_banned(pgsdata, id):
    return conf.send_some(pgsdata, f"INSERT INTO banned (tg_person) VALUES ({str(id)})")

def delete_ban(pgsdata, id):
    return conf.send_some(pgsdata, f"DELETE FROM banned WHERE tg_person={str(id)}")

def check_ban(pgsdata, id):
    return conf.select_one(pgsdata, f"SELECT COUNT(*) FROM banned WHERE tg_person='{str(id)}'")[0]

def check_all_ban(pgsdata):
    return conf.select_all(pgsdata, f"SELECT * FROM banned")
   