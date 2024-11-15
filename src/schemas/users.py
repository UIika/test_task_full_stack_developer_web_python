from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class UserRead(UserBase):
    id: int
    is_superuser: bool

class UserCreate(UserBase):    
    password: str
    
class UserCreateAdmin(UserCreate):
    is_superuser: bool = False

