import mysql.connector

import table.work_with_database.conf_mysql as conf

def put_admin(mysqldata, id):
    return conf.send_some(mysqldata, f"INSERT INTO admin (tg_person) VALUES ({str(id)})")

def delete_admin(mysqldata, id):
    return conf.send_some(mysqldata, f"DELETE FROM admin WHERE tg_person={str(id)})")

def check_admin(mysqldata, id):
    return conf.select_one(mysqldata, f"SELECT COUNT(*) FROM admin WHERE tg_person={str(id)}")

def check_all_admin(mysqldata):
    return conf.select_all(mysqldata, f"SELECT tg_person FROM admin")
