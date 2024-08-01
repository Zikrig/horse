import psycopg2
from psycopg2 import Error

import table.work_with_database.conf as conf

def person_gen(pgsdata, person_data):
    p = select_person(pgsdata, person_data[0])
    if len(p) == 0:
        put_person(pgsdata, person_data)
    else:
        alt_person(pgsdata, person_data)

def put_person(pgsdata, pd):
    return conf.send_some(pgsdata, f"INSERT INTO people(tg_person, name, phone, describe, photo) VALUES ('{pd[0]}','{pd[1]}','{pd[2]}','{pd[3]}','{pd[4]}')")

def alt_person(pgsdata, pd):
    return conf.send_some(pgsdata, f"UPDATE people SET (name, phone, describe, photo) = ('{pd[1]}', '{pd[2]}', '{pd[3]}', '{pd[4]}') WHERE tg_person={str(pd[0])}")

def alt_person_field(pgsdata, id, field, mean):
    return conf.send_some(pgsdata, f"UPDATE people SET {field} = '{mean}' WHERE tg_person='{str(id)}'")

def del_person(pgsdata, id):
    return conf.send_some(pgsdata, f"DELETE FROM people WHERE tg_person='{str(id)}'")

def select_person(pgsdata, tg_id):
    return conf.select_one(pgsdata, f"SELECT * FROM people WHERE tg_person='{str(tg_id)}'")

def select_all_person(pgsdata):
    return conf.select_all(pgsdata, f"SELECT * FROM people")
