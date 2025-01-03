import os
from local_data import LocalData

images_dir = os.path.abspath('').replace('\\', '/') + '/telegram/data/images'
avas_dir = images_dir+'/avas'
horseh_dir = images_dir+'/horseh'

textes_dir = os.path.abspath('').replace('\\', '/') + '/telegram/data/texts'

holiday_dir = os.path.abspath('').replace('\\', '/') + '/telegram/data/holiday'

holiday_files = {
    'weekdays': holiday_dir + '/weekdays.txt',
    'another': holiday_dir + '/anotherdays.txt'
}

hh_files = {
    'coords':   '/coords.txt',
    'description': '/describe.txt',
    'photos': '/photo_paths.txt'
}

# pgsdata = {
#     'dbname':"postgres",
#     'user':"postgres",
#     # 'password':"password",
#     'password':'httphuggingfapaceTSAGITSArenamapuserpass',
#     # 'host':"db",
#     'host': '127.0.0.1',
#     # 'port':"5433"
#     'port':"5432"
# }

mysqldata={
    'user':'root2', 
    'password':'T!Mak~_3AdHK ',
    'host':'127.0.0.1',
    'database':'mydb'
}
lc = LocalData(hh_files, textes_dir, horseh_dir, holiday_files)