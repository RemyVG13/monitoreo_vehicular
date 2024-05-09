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

def carsEntity(entity) -> list:
    return [carEntity(item) for item in entity]