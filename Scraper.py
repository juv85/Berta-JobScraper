import datetime
import re

d = '06.07.2023 | '

def date_clean(d):
    md = re.sub('[' ', |]', '', d)
    md = md.split('.')
    yr = int(md[2])
    mth = int(md[1])
    day = int(md[0])
    print(md)


    _date = datetime.datetime(yr, mth, day)
    date = _date.strftime("%b-%d-%Y")

    print(date)

date_clean(d)