import psycopg2
from psycopg2 import Error

def select_one(pgsdata, zap):
    try:
        conn = psycopg2.connect(
            dbname=pgsdata['dbname'],
            user=pgsdata['user'], 
            password=pgsdata['password'], 
            host=pgsdata['host'], 
            port=pgsdata['port']
            )
        conn.autocommit = True  # устанавливаем актокоммит
        
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()  
        res = cursor.fetchone()

        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        res = []
        print(f'Ошибка {error}')
    finally:
        # if cursor:
        #     cursor.close()
        # if conn:
        #     conn.close()
        return res

def select_all(pgsdata, zap, rasp=True):
    try:
        conn = psycopg2.connect(
            dbname=pgsdata['dbname'],
            user=pgsdata['user'], 
            password=pgsdata['password'], 
            host=pgsdata['host'], 
            port=pgsdata['port']
            )
        conn.autocommit = True  # устанавливаем актокоммит
        
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()  

        res = cursor.fetchall()

    except (Exception, Error) as error:
        res = []
        print(f'Ошибка {error}')
    finally:
        # if cursor:
        #     cursor.close()
        # if conn:
        #     conn.close()
        if rasp:
            res = list(set([r[0] for r in res]))
        return res

def send_some(pgsdata, zap):
    try:
        conn = psycopg2.connect(
            dbname=pgsdata['dbname'],
            user=pgsdata['user'], 
            password=pgsdata['password'], 
            host=pgsdata['host'], 
            port=pgsdata['port']
            )
        conn.autocommit = True  # устанавливаем актокоммит
        
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()  

    except (Exception, Error) as error:
        print(f'Ошибка {error}')
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if conn:
    #         conn.close()