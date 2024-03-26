from datetime import datetime, timedelta
from time import mktime

def regional_timezone(hour : int = 0):
    if hour == 0:
        return datetime.utcnow()
    else:
        if hour > 0:
            return (datetime.utcnow() + timedelta(hours=abs(hour)))
        else:
            return (datetime.utcnow() - timedelta(hours=abs(hour)))

def date_to_seconds(date: datetime):
    return mktime(date.timetuple())

def seconds_to_date(seconds: int):
    return datetime.fromtimestamp(seconds)

def bolivia_datetime():
    return regional_timezone(-4)

def is_past_date(date: datetime):
    
    return False

def bolivia_datetime_seconds():
    return date_to_seconds(bolivia_datetime())
#def date_to_seconds():
#    date = datetime.utcnow() - timedelta(hours=4)
#    return mktime(date.timetuple())
#
