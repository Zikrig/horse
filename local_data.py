from config import *
import os.path, os
from datetime import datetime, timedelta

import telegram.states_work.time_changer as tc

class LocalData:
    def __init__(self, hh_files, textes_dir, horseh_dir, holiday_files):
        self.hh_files = hh_files
        self.horseh_dir = horseh_dir
        self.textes_dir = textes_dir
        self.holiday_files = holiday_files

        self.imgs = []
        self.imgs_clear = []

        self.days = [
            'Понедельник',
            'Вторник',
            'Среда',
            'Четверг',
            'Пятница',
            'Суббота',
            'Воскресенье'
        ]

        self.weekdays = self.get_weekdays()
        self.justdays = self.get_justdays()
        self.justdays.sort()
        self.justdays_strs = [datetime.strftime(d, '%Y-%m-%d') for d in self.justdays]

        if('coords' in self.hh_files):
            if(os.path.exists(textes_dir+self.hh_files['coords'])):
                self.init_coords()
        if('describe' in self.hh_files):
            if(os.path.exists(textes_dir+self.hh_files['describe'])):
                self.init_describe()

        if('photos' in self.hh_files):
            self.init_photos()

    def init_coords(self):
        f = open(self.textes_dir+self.hh_files['coords'], 'r')
        t = f.read()
        f.close()
        coords = t.split('\n')
        if(len(coords)>1):
            self.coord1 = float(coords[0]) 
            self.coord2 = float(coords[1])
    
    def init_describe(self):
        f = open(self.textes_dir+self.hh_files['describe'], 'r', encoding='utf-8')
        t = f.read()
        f.close()
        self.describe = t

    def init_photos(self):
        f = open(self.textes_dir+self.hh_files['photos'], 'r', encoding='utf-8')
        t = f.read()
        f.close()
        imgs = t.split('\n')
        for st in imgs:
            posint = self.horseh_dir + st
            if(os.path.exists(posint)):
                self.imgs.append(posint)
                self.imgs_clear.append(st)

    def set_descr(self, descr):
        self.describe = descr
        f = open(self.textes_dir+self.hh_files['describe'], 'w', encoding='utf-8')
        f.write(descr)
        f.close

    def set_coords(self, crds):
        all_coords = crds.split('\n')
        if(not len(all_coords)>1):
            return False
        self.coord1, self.coord2 = float(all_coords[0]), float(all_coords[1])
        f = open(self.textes_dir+self.hh_files['coords'], 'w', encoding='utf-8')
        f.write(crds)
        f.close

    def del_photo_by_num(self, num):
        if num > len(self.imgs)-1:
            return True
        imgpath = self.imgs[num]
        if(not os.path.exists(imgpath)):
            return True
        self.imgs_clear.pop(num)
        self.imgs.pop(num)
        os.remove(imgpath)
        f = open(self.textes_dir+self.hh_files['photos'], 'w', encoding='utf-8')
        f.write('\n'.join(self.imgs_clear))
        f.close()
        
    def add_photo_to_file(self, name):
        self.imgs.append(self.horseh_dir+'/'+name)
        self.imgs_clear.append('/'+name)
        f = open(self.textes_dir+'/'+self.hh_files['photos'], 'w', encoding='utf-8')
        f.write('\n'.join(self.imgs_clear))
        f.close()

    def get_weekdays(self):
        f = open(self.holiday_files['weekdays'], 'r')
        days_rude = f.read()
        f.close()

        days_str = days_rude.split('\n')
        days = [int(d) for d in days_str]
        self.weekdays = days
        return days
    
    def set_weekdays(self, days):
        f = open(self.holiday_files['weekdays'], 'w')
        f.write('\n'.join([str(day) for day in days]))
        f.close()

    def change_weekday(self, num):
        if(self.weekdays[num] == 0):
            self.weekdays[num] = 1
        else:
            self.weekdays[num] = 0

        self.set_weekdays(self.weekdays)

    def get_justdays(self):
        f = open(self.holiday_files['another'], 'r')
        days_rude = f.read()
        f.close()

        days_str = days_rude.split('\n')
        if '' in days_str:
            days_str.remove('')
        days = [datetime.strptime(d, '%Y-%m-%d').date() for d in days_str]
        self.justdays = days
        self.justdays_strs = days_str
        return days
    
    def remove_from_justdays(self, day):
        days_strs = [datetime.strftime(d, '%Y-%m-%d') for d in self.justdays]
        if(day in days_strs):
            k = days_strs.index(day)
        else:
            return False
        
        days_strs.pop(k)
        self.justdays.pop(k)
        self.set_justdays(days_strs)
        self.justdays_strs = days_strs
        return True
        
    def add_to_justdays(self, day):
        self.justdays_strs.append(day)
        self.set_justdays(self.justdays_strs)
            
    def set_justdays(self, days):
        self.justdays = [datetime.strptime(d, '%Y-%m-%d').date() for d in days]
        f = open(self.holiday_files['another'], 'w')
        f.write('\n'.join(days))
        f.close()

    def pretty_weekdays(self):
        res = ''
        
        for day in range(len(self.weekdays)):
            if(self.weekdays[day] == 1):
                res += '<b>'+'\n' + self.days[day]+"</b>"
        if res == '':
            res = '\nнет'
        return res
    
    def get_justdays_list_for_90(self):
        res_list = []
        for day in self.justdays:
            if day > datetime.today().date() and day < (datetime.today() + timedelta(days=90)).date():
                res_list.append(day)
        return res_list
    
    def pretty_justdays(self):
        res_list = self.get_justdays_list_for_90()
        res_list = [tc.date_to_str(r) for r in res_list]
        res = ''
        if(len(res_list) != 0):
            res += '<b>'+'\n'.join(res_list)+"</b>"
        else:
            res += '<b>Особых выходных нет.</b>'
        return res
    
    def is_day_holiday(self, day):
        print('Проверяем дату')
        if isinstance(day, str):
            day_str = day
            day_date = datetime.strptime(day, '%Y-%m-%d')
        else:
            day_str = datetime.strftime(day, '%Y-%m-%d')
            day_date = day
        
        weekday_num = day_date.isoweekday()
        if self.weekdays[weekday_num] == 1:
            return False
        if day_str in self.justdays_strs:
            return False
        return True

    def holidays_pretty_hide(self):
        txt_dop = '\nОбратите внимание!\n'
        weeks = self.pretty_weekdays()
        if len(weeks) > 5:
            txt_dop1 = f'Выходные дни вашей конюшни: {self.pretty_weekdays()}'
        else:
            txt_dop1 = ''
        if len(self.justdays_strs) > 0:
            txt_dop2 = f'\nОсобые выходные в будущие три месяца:\n{self.pretty_justdays()}'
        else:
            txt_dop2 = ''

        if txt_dop1 == '' and txt_dop2 == '':
            txt_dop_all = ''
        else:
            txt_dop_all = txt_dop + txt_dop1 + txt_dop2   
        
        return txt_dop_all