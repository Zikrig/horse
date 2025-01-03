import psycopg2
from psycopg2 import Error

def select_one(my, zap):
    try:
        conn = psycopg2.connect(
            database = my['dbname'],
            user=my['user'], 
            password=my['password'],
            host=my['host'])
        conn.autocommit = True
        
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()  
        res = cursor.fetchone()
        if res == None:
            res = []
        cursor.close()
        conn.close()
    except (Exception, Error) as error:
        res = []
        print(f'Ошибка {error}')
        # res = error
    finally:
        return res
        
def select_all(my, zap, rasp=True):
    try:
        conn = psycopg2.connect(
            database = my['dbname'],
            user=my['user'], 
            password=my['password'],
            host=my['host'])
        conn.autocommit = True
        
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()  
        
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        
    except Error as error:
        print(f'Ошибка {error}')
        res = []
        return res
    finally:
        # if rasp:
        #     res = list(set([r[0] for r in res]))
        return res

def send_some(my, zap):
    # print('send')
    try:
        conn = psycopg2.connect(
            database = my['dbname'],
            user=my['user'], 
            password=my['password'],
            host=my['host'])
        # conn.autocommit = True
        # print('try')
        cursor = conn.cursor()
        cursor.execute(zap)
        conn.commit()    

    except Error as error:
        print(f'Ошибка {error}')
        res = error
        return res
    finally:
        # print('fin')
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
