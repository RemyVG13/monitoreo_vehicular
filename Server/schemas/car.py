def carEntity(item) -> dict:
    entity = {
        "id": str(item["_id"]),
        "name": item["name"],
        "plate": item["plate"],
        "make": item["make"],
        "model": item["model"],
        "year": item["year"],
        "thingspeak_id": item["thingspeak_id"],
        "disabled": item["disabled"],
        "creation_date_inseconds": item["creation_date_inseconds"],
        "creator_id": item["creator_id"],
        "history_element": item["history_element"],
        "deleted": item["deleted"],
    }
    return entity

def carMapEntity(item) -> dict:
    entity = {
        "id": str(item["_id"]),
        "name": item["name"],
        "plate": item["plate"],
        "make": item["make"],
        "model": item["model"],
        "year": item["year"],
        "thingspeak_id": item["thingspeak_id"],
        "full_name": item["full_name"],
        "teacher_name": item["teacher_name"],
        "longitude": item["longitude"],
        "latitude": item["latitude"],
        "fuel": item["fuel"],
        "speed": item["speed"],
        "state": item["state"],
        "zone": item["zone"],
        "is_working": item["is_working"],
        "teacher_id": item["teacher_id"],
        "last_time": item["last_time"]
    }
    return entity

def carsEntity(entity) -> list:
    return [carEntity(item) for item in entity]