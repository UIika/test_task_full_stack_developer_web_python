from pydantic import BaseModel


class FileCreate(BaseModel):
    filename: str
    is_private: bool

class FileUpdate(FileCreate):
    downloads: int
    