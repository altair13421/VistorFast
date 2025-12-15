from pydantic import BaseModel

class AnilistBase(BaseModel):
    name: str
    description: str

class AnilistCreate(AnilistBase):
    pass

class Anilist(AnilistBase):
    id: int

    class Config:
        from_attributes = True
