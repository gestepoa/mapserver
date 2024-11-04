# app/database/models.py
from sqlalchemy import Column, Integer, String, Float
from app.database.config import Base

class MapPoint(Base):
    __tablename__ = "map_points"

    id = Column(Integer, primary_key=True, comment="履历信息id")
    spot_name = Column(String(255), nullable=False, unique=False, comment="履历信息id")
    country_name = Column(String(255), nullable=True, comment="履历信息id")
    note = Column(String(255), nullable=True, comment="履历信息id")
    latitude = Column(Float, nullable=False, comment="履历信息id")
    longitude = Column(Float, nullable=False, comment="履历信息id")
    height = Column(Float, nullable=True, comment="履历信息id")
