from datetime import datetime, timedelta,timezone
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
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    time_of_day = base_date + timedelta(seconds=timestamp)
    formatted_time = time_of_day.strftime("%I:%M %p")
    return formatted_time


def iso_to_local_time(iso_date: str):
    # Eliminar la 'Z' y convertir la cadena ISO 8601 a un objeto datetime asumiendo UTC
    date_utc = datetime.strptime(iso_date.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
    date_utc = date_utc.replace(tzinfo=timezone.utc)
    local_date = date_utc.astimezone()
    day_name = local_date.strftime("%A")
    days_translation = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    day_name_es = days_translation.get(day_name, "Día desconocido")
    formatted_time = local_date.strftime("%I:%M %p")
    midnight = local_date.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = (local_date - midnight).seconds
    daytime = {}
    daytime["day"] = day_name_es
    daytime["hour"] = formatted_time
    #timestamp
    daytime["timestamp"] = seconds_since_midnight
    return daytime

def get_current_time_in_bolivia_seconds():
    bolivia_timezone = timezone(timedelta(hours=-4))
    now_utc = datetime.now(timezone.utc)
    now_in_bolivia = now_utc.astimezone(bolivia_timezone)
    midnight_in_bolivia = now_in_bolivia.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_since_midnight = (now_in_bolivia - midnight_in_bolivia).seconds
    return seconds_since_midnight

def get_current_weekday_in_bolivia():
    bolivia_timezone = timezone(timedelta(hours=-4))
    now_utc = datetime.now(timezone.utc)
    now_in_bolivia = now_utc.astimezone(bolivia_timezone)
    day_name_english = now_in_bolivia.strftime('%A')
    days_translation = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    day_name_spanish = days_translation[day_name_english]

    return day_name_spanish

def is_within_last_minute(iso_date_str):
    received_date = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
    current_date = datetime.now(timezone.utc)
    time_difference = current_date - received_date
    return time_difference < timedelta(minutes=1)


def convert_to_bolivia_time(iso_date):
    date_obj = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
    bolivia_time = date_obj - timedelta(hours=4)
    date_str = bolivia_time.strftime("%d de %B, %Y. A las %I:%M %p")
    date_str = date_str.replace("AM", "AM").replace("PM", "PM")
    spanish_months = {
        "January": "Enero", "February": "Febrero", "March": "Marzo",
        "April": "Abril", "May": "Mayo", "June": "Junio",
        "July": "Julio", "August": "Agosto", "September": "Septiembre",
        "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    for eng, esp in spanish_months.items():
        date_str = date_str.replace(eng, esp)

    return date_str
