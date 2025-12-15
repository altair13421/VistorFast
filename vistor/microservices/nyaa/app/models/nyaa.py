from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Nyaa(Base):
    __tablename__ = "nyaas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
