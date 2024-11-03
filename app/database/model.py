# app/database/models.py
from sqlalchemy import Column, Integer, String, Float
from app.database.config import Base

class MapPoint(Base):
    __tablename__ = "map_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
