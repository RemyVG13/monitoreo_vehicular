def alarmEntity(item) -> dict:
    entity = {
        "id": str(item["_id"]),
        "date": item["date"],
        "hour": item["hour"],
        "reason": item["reason"],
        "teacher_name": item["teacher_name"],
        "car_name": item["car_name"],
        "disabled": item["disabled"],
        "creation_date_inseconds": item["creation_date_inseconds"],
        "creator_id": item["creator_id"],
        "history_element": item["history_element"],
        "deleted": item["deleted"],
    }
    return entity

def alarmsEntity(entity) -> list:
    return [alarmEntity(item) for item in entity]