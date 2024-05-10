
def userEntity(item) -> dict:
    
    if("username" not in item):
        item["username"] = ""
    if("password" not in item):
        item["password"] = ""
    entity = {
        "id": str(item["_id"]),
        "first_name": item["first_name"],
        "father_last_name": item["father_last_name"],
        "mother_last_name": item["mother_last_name"],
        "id_number": item["id_number"],
        "id_zone": item["id_zone"],
        "username": item["username"],
        "password": item["password"],
        "rol": item["rol"],
        "birthday_date_inseconds": item["birthday_date_inseconds"],
        "disabled": item["disabled"],
        "creation_date_inseconds": item["creation_date_inseconds"],
        "creator_id": item["creator_id"],
        "history_element": item["history_element"],
        "deleted": item["deleted"],
    }
    return entity

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]