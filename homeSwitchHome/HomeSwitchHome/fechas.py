from datetime import timedelta
from datetime import date

def get_start_end_dates(year, week):
     d = date(year,1,1)
     if(d.isoweekday()<= 3):
         d = d - timedelta(d.isoweekday())             
     else:
         d = d + timedelta(7-d.isoweekday())
     dlt = timedelta(days = (week-1)*7)
     return d + dlt,  d + dlt + timedelta(days=6)


fe=date
fe= date.today()
print((get_start_end_dates(fe.isocalendar()[0], fe.isocalendar()[1]))[0])
