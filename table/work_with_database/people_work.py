
from table.work_with_database import conf_mysql as conf

def person_gen(mysqldata, person_data):
    p = select_person(mysqldata, person_data[0])
    if len(p) == 0:
        put_person(mysqldata, person_data)
    else:
        alt_person(mysqldata, person_data)

def put_person(mysqldata, pd):
    return conf.send_some(mysqldata, f"INSERT INTO people(tg_person, name, phone, description, photo) VALUES ({pd[0]},'{pd[1]}','{pd[2]}','{pd[3]}','{pd[4]}')")

def alt_person(mysqldata, pd):
    return conf.send_some(mysqldata, f"UPDATE people SET (name, phone, description, photo) = ('{pd[1]}', '{pd[2]}', '{pd[3]}', '{pd[4]}') WHERE tg_person={str(pd[0])}")

def alt_person_field(mysqldata, id, field, mean):
    return conf.send_some(mysqldata, f"UPDATE people SET {field} = '{mean}' WHERE tg_person={str(id)}")

def del_person(mysqldata, id):
    return conf.send_some(mysqldata, f"DELETE FROM people WHERE tg_person={str(id)}")

def select_person(mysqldata, tg_id):
    return conf.select_one(mysqldata, f"SELECT * FROM people WHERE tg_person={str(tg_id)}")

def select_all_person(mysqldata):
    return conf.select_all(mysqldata, f"SELECT * FROM people")
