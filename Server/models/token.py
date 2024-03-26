from pydantic import BaseModel, Field

class LoginForm(BaseModel):
    username: str
    password: str