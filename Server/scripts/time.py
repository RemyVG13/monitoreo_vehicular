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

def seconds_to_hhmm(timestamp: int):
    # Crear una fecha base, que será la medianoche del día actual
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Añadir el timestamp como un delta de tiempo a la fecha base
    time_of_day = base_date + timedelta(seconds=timestamp)

    # Formatear la hora en el formato deseado "HH:MM AM/PM"
    formatted_time = time_of_day.strftime("%I:%M %p")
    return formatted_time
    print(formatted_time)

