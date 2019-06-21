from datetime import timedelta, datetime
from datetime import date
from calendar import monthrange

def get_start_end_dates(year, week):
     d = date(year,1,1)
     if(d.isoweekday()<= 3):
         d = d - timedelta(d.isoweekday())             
     else:
         d = d + timedelta(7-d.isoweekday())
     dlt = timedelta(days = (week-1)*7)
     return d + dlt,  d + dlt + timedelta(days=6)


def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta