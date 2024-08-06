from table.work_with_database import conf_mysql as conf

def put_banned(mysqldata, id):
    return conf.send_some(mysqldata, f"INSERT INTO banned (tg_person) VALUES ({str(id)})")

def delete_ban(mysqldata, id):
    return conf.send_some(mysqldata, f"DELETE FROM banned WHERE tg_person={str(id)}")

def check_ban(mysqldata, id):
    return conf.select_one(mysqldata, f"SELECT COUNT(*) FROM banned WHERE tg_person={str(id)}")[0]

def check_all_ban(mysqldata):
    return conf.select_all(mysqldata, f"SELECT * FROM banned")
   