from pydantic import BaseModel

class FileList(BaseModel):
    id: int
    filename: str
    size: int

    class Config:
        from_attributes = True

class NyaaBase(BaseModel):
    name: str
    description: str
    magnet_link: str

class NyaaCreate(NyaaBase):
    pass

class Nyaa(NyaaBase):
    id: int

    class Config:
        from_attributes = True
