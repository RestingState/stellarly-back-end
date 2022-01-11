from app import Base
from app.models import Table, Column, Integer, ForeignKey, VARCHAR
from sqlalchemy import BigInteger, Date


# user_category = Table('user_category', Base.metadata,
#                       Column('user_id', ForeignKey('user.id'), primary_key=True),
#                       Column('category_id', ForeignKey('category.id'), primary_key=True))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False, unique=True)
    password = Column(VARCHAR, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'))
    username = Column(VARCHAR, nullable=False, unique=True)


# class Category(Base):
#     __tablename__ = 'category'
#     id = Column(Integer, primary_key=True)
#     name = Column(VARCHAR, nullable=False)


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)


class Satellites(Base):
    __tablename__ = 'satellites'
    norad_id = Column(BigInteger, primary_key=True)
    satname = Column(VARCHAR, nullable=False)
    owner = Column(VARCHAR, nullable=False)
    launchdate = Column(Date, nullable=False)
    launchsite = Column(VARCHAR, nullable=False)
    inclination = Column(VARCHAR, nullable=False)
    ascending_node_longitude = Column(VARCHAR, nullable=False)
    eccentricity = Column(VARCHAR, nullable=False)
    pericenter_argument = Column(VARCHAR, nullable=False)
    average_anomaly = Column(VARCHAR, nullable=False)
    call_frequency = Column(VARCHAR, nullable=False)


class Stars(Base):
    __tablename__ = 'stars'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR)
    right_ascension = Column(VARCHAR)
    declination = Column(VARCHAR)
    flux_visible_light = Column(VARCHAR)
    parallax = Column(VARCHAR)
    spectral_type = Column(VARCHAR)
