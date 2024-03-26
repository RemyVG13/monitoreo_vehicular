def carDataEntity(item) -> dict:
    entity = {
        "id": str(item["_id"]),
        "id_car": item["id_car"],
        "date_in_seconds": item["date_in_seconds"],
        "fuel": item["fuel"],
        "latitude": item["latitude"],
        "longitude": item["longitude"],
        "speed": item["speed"],
        "disabled": item["disabled"],
        "creation_date_inseconds": item["creation_date_inseconds"],
        "creator_id": item["creator_id"],
        "history_element": item["history_element"],
        "deleted": item["deleted"],
    }
    return entity

def carDatasEntity(entity) -> list:
    return [carDataEntity(item) for item in entity]