from sqlalchemy import create_engine, ForeignKey, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

import datetime

from db.db_connection import CONNECTION_STRING

class Base(DeclarativeBase):
    pass

class Astro(Base):
    __tablename__ = 'astro'

    astro_id: Mapped[int] = mapped_column(primary_key=True)

    go_outside: Mapped[bool]

    sunrise: Mapped[datetime.time]

    sunset: Mapped[datetime.time]

    moonrise: Mapped[datetime.time]

    moonset: Mapped[datetime.time]

    moon_phase: Mapped[str]

    moon_illumination: Mapped[int]

    weather_id: Mapped[int] = mapped_column(ForeignKey('weather.weather_id'))

engine = create_engine(CONNECTION_STRING, echo=True)

session = Session(engine)

go_outside_base_data = session.execute(select(Astro.astro_id, Astro.sunset)).all()

outside_threshold = datetime.time(hour=18)
for astro_id, sunset in go_outside_base_data:
    session.execute(update(Astro).where(Astro.astro_id == astro_id).values(go_outside=sunset > outside_threshold))

session.commit()
session.close()