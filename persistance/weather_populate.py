from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, validates

import datetime

from db.db_connection import CONNECTION_STRING

class Base(DeclarativeBase):
    pass

class Weather(Base):
    __tablename__ = 'weather'

    weather_id: Mapped[int] = mapped_column(primary_key=True)

    country: Mapped[str]

    wind_degree: Mapped[int]

    wind_kph: Mapped[float]

    wind_direction: Mapped[str]

    last_updated: Mapped[datetime.datetime]

    sunrise: Mapped[datetime.time]

    sunset: Mapped[datetime.time]

    moonrise: Mapped[datetime.time]

    moonset: Mapped[datetime.time]

    @validates('moonset')
    def validate_moonset(self, key, moonset):
        if moonset == 'No moonset':
            return None
        else:
            spt = datetime.datetime.strptime(moonset, "%I:%M %p")
            sft = datetime.datetime.strftime(spt, "%H:%M")
            return sft
        
    @validates('sunrise', 'sunset', 'moonrise')
    def validate_time(self, key, time):
        spt = datetime.datetime.strptime(time, "%I:%M %p")
        sft = datetime.datetime.strftime(spt, "%H:%M")
        return sft

    moon_phase: Mapped[str]

    moon_illumination: Mapped[int]


engine = create_engine(CONNECTION_STRING, echo=True)

session = Session(engine)

from pathlib import Path
import csv

weather_file = Path('data/GlobalWeatherRepository.csv')
reader = csv.DictReader(open(weather_file))

# Стандартні дані
cols = ['country', 'wind_degree', 'wind_kph', 'wind_direction', 'last_updated']
# Додаткові за варіантом 4. Схід-Захід небесних тіл
astro = ['sunrise', 'sunset', 'moonrise', 'moonset', 'moon_phase', 'moon_illumination']

for i, row in enumerate(reader):
    session.add(Weather(weather_id=i, **{key:row[key] for key in cols + astro}))

session.flush()
session.commit()
session.close()