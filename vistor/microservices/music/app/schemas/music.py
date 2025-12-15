from pydantic import BaseModel

class MusicBase(BaseModel):
    name: str
    description: str

class MusicCreate(MusicBase):
    pass

class Music(MusicBase):
    id: int

    class Config:
        from_attributes = True
