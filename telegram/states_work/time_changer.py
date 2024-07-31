def time_to_str(time):
    return time.strftime("%H:%M")

def date_to_str(date, with_year=True):
    mm, dd, yy = date.month, date.day, date.year
    yy = ' '+str(yy) if with_year else ''
    return f'{dd} {create_mounth_from_num(mm)}{yy}'

def create_mounth_from_num(num):
    months  = ('Января' , 'Февраля' , 'Марта' , 'Апреля' , 'Мая' , 'Июня' , 'Июля' , 'Августа' , 'Сентября' , 'Октября' , 'Ноября' , 'Декабря')
    return months[int(num) - 1].lower()