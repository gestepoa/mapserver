# app/database/models.py
from sqlalchemy import Column, Integer, String, Float
from app.database.config import Base

class MapPoint(Base):
    __tablename__ = "map_points"

    id = Column(Integer, primary_key=True, comment="id")
    spot_name = Column(String(255), nullable=False, unique=False, comment="点位名称")
    spot_short_name = Column(String(255), nullable=True, unique=False, comment="点位简称")
    spot_name_EN = Column(String(255), nullable=True, unique=False, comment="点位英文名称")
    spot_short_name_EN = Column(String(255), nullable=True, unique=False, comment="点位英文简称")
    country_name = Column(String(255), nullable=True, comment="所属国家")
    country_capital = Column(String(255), nullable=True, comment="所属国首都")
    continental = Column(String(255), nullable=True, comment="所属大洲")
    district = Column(String(255), nullable=True, comment="所属地区")
    note = Column(String(255), nullable=True, comment="备注")
    latitude = Column(Float, nullable=False, comment="纬度")
    longitude = Column(Float, nullable=False, comment="经度")
    height = Column(Float, nullable=True, comment="高程")


class CountryInfo(Base):
    __tablename__ = "country_info"

    id = Column(Integer, primary_key=True, comment="id")
    country_name = Column(String(255), nullable=False, unique=False, comment="国家名称")
    capital = Column(String(255), nullable=True, unique=False, comment="首都")
    biggest_city= Column(String(255), nullable=True, unique=False, comment="最大城市")
    population = Column(String(255), nullable=True, unique=False, comment="人口")
    en_name = Column(String(255), nullable=True, comment="英文名称")
    continental = Column(String(255), nullable=True, comment="所属大洲")
    district = Column(String(255), nullable=True, comment="所属地区")
    note = Column(String(255), nullable=True, comment="备注")

