import table.work_with_database.conf_pgs as conf

def put_admin(pgsdata, id):
    return conf.send_some(pgsdata, f"INSERT INTO admin (tg_person) VALUES ({str(id)})")

def delete_admin(pgsdata, id):
    # Исправлено: убрана лишняя скобка
    return conf.send_some(pgsdata, f"DELETE FROM admin WHERE tg_person={str(id)}")

def check_admin(pgsdata, id):
    return conf.select_one(pgsdata, f"SELECT COUNT(*) FROM admin WHERE tg_person={str(id)}")[0]

def check_all_admin(pgsdata):
    return conf.select_all(pgsdata, "SELECT tg_person FROM admin")
