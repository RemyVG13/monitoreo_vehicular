def scheduleEntity(item) -> dict:
    entity = {
        "id": str(item["_id"]),
        "teacher_id": item["teacher_id"],
        "car_id": item["car_id"],
        "day": item["day"],
        "hour": item["hour"],
        "disabled": item["disabled"],
        "creation_date_inseconds": item["creation_date_inseconds"],
        "creator_id": item["creator_id"],
        "history_element": item["history_element"],
        "deleted": item["deleted"],
    }
    return entity

def schedulesEntity(entity) -> list:
    return [scheduleEntity(item) for item in entity]