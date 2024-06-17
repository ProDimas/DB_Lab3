from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

import datetime

from db.db_connection import CONNECTION_STRING

class Base(DeclarativeBase):
    pass

class Weather(Base):
    __tablename__ = 'weather'

    weather_id: Mapped[int] = mapped_column(primary_key=True)

    sunrise: Mapped[datetime.time]

    sunset: Mapped[datetime.time]

    moonrise: Mapped[datetime.time]

    moonset: Mapped[datetime.time]

    moon_phase: Mapped[str]

    moon_illumination: Mapped[int]

class Astro(Base):
    __tablename__ = 'astro'

    astro_id: Mapped[int] = mapped_column(primary_key=True)

    sunrise: Mapped[datetime.time]

    sunset: Mapped[datetime.time]

    moonrise: Mapped[datetime.time]

    moonset: Mapped[datetime.time]

    moon_phase: Mapped[str]

    moon_illumination: Mapped[int]

    weather_id: Mapped[int] = mapped_column(ForeignKey('weather.weather_id'))

    def __init__(self, astro_id, weather: Weather):
        self.astro_id = astro_id
        for col in weather.__table__.c.keys():
            self.__setattr__(col, weather.__getattribute__(col))


engine = create_engine(CONNECTION_STRING, echo=True)

session = Session(engine)

weather_rows = session.scalars(select(Weather)).all()

for i, row in enumerate(weather_rows):
    session.add(Astro(astro_id=i, weather=row))

session.flush()
session.commit()
session.close()