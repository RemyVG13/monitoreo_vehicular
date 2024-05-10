def scheduleDetailEntity(item) -> dict:
    entity = {
        "id": str(item["_id"]),
        "teacher_id": item["teacher_id"],
        "teacher_name": item["teacher_name"],
        "car_id": item["car_id"],
        "car_name": item["car_name"],
        "day": item["day"],
        "hour": item["hour"],
        "hour_hhmm": item["hour_hhmm"],
    }
    return entity

def schedulesDetailEntity(entity) -> list:
    return [scheduleDetailEntity(item) for item in entity]