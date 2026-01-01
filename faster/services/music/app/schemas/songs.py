
from pydantic import BaseModel, Field

class SongBase(BaseModel):
    id: int
    title: str
    duration: int = Field(..., description="Duration of the song in seconds")
    times_played: int = Field(0, description="Number of times the song has been played")

    class Config:
        orm_mode = True
