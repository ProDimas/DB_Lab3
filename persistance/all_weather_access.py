from sqlalchemy import create_engine, ForeignKey, select, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

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

    astro: Mapped['Astro'] = relationship(back_populates='weather')

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

    weather: Mapped['Weather'] = relationship(back_populates='astro')

class AllWeatherDAO:
    def __init__(self):
        pass

    def connect(self):
        self.engine = create_engine(CONNECTION_STRING)
        self.session = Session(self.engine)

    def res_to_string(self, res):
        s_res = []
        for r in res:
            w, a = r
            s_res.append(f'''All weather:
weather_id: {w.weather_id}
country: {w.country}
wind_degree: {w.wind_degree}
wind_kph: {w.wind_kph}
wind_direction: {w.wind_direction}
last_updated: {w.last_updated}
astro_id: {a.astro_id}
go_outside: {a.go_outside}
sunrise: {a.sunrise}
sunset: {a.sunset}
moonrise: {a.moonrise}
moonset: {a.moonset}
moon_phase: {a.moon_phase}
moon_illumination: {a.moon_illumination}''')
        return '\n'.join(s_res)

    def read(self, country, last):
        res = self.session.execute(select(Weather, Astro).join(Astro.weather).where(and_(Weather.country == country,
                                                                          Weather.last_updated == last))).all()
        return self.res_to_string(res)
    
    def disconnect(self):
        self.session.close()