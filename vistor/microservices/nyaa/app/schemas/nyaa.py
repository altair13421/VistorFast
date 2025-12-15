from pydantic import BaseModel

class NyaaBase(BaseModel):
    name: str
    description: str

class NyaaCreate(NyaaBase):
    pass

class Nyaa(NyaaBase):
    id: int

    class Config:
        from_attributes = True
