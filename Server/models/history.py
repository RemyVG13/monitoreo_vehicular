from pydantic import BaseModel
from typing import Union

class History(BaseModel):
    date_inseconds: Union[int, None] = None
    modifier_user_id: Union[str, None] = None
    table_name: Union[str, None] = None
    table_element_id: Union[str, None] = None
    modifier_user_id: Union[str, None] = None
    previous_content_element_id: Union[str, None] = None
    new_content_element_id: Union[str, None] = None
    