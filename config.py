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

pgsdata = {
    'dbname':"postgres",
    'user':"postgres",
    'password':'12345',
    'host': 'localhost',
#     'user':"root",
#     'password':'bU9oR9zU7g',
#     'host': 'localhost',
    'port':"5432"
}

lc = LocalData(hh_files, textes_dir, horseh_dir, holiday_files)