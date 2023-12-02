import sqlalchemy as sqal
from sqlalchemy.orm import sessionmaker, declarative_base
import time
base = declarative_base()
class ForecastData(base):
    __tablename__ = "forcasts"

    hash = sqal.Column('hash', sqal.Float, primary_key=True)
    date = sqal.Column('date', sqal.DateTime)
    provider = sqal.Column('provider', sqal.String)
    xcoord = sqal.Column('xcoord', sqal.Float)
    ycoord = sqal.Column('ycoord', sqal.Float)
    forecastdelta = sqal.Column('forecastdelta', sqal.Float)
    temperature = sqal.Column('temperature', sqal.Float)
    windGustsKmh = sqal.Column('windGustsKmh', sqal.Float)
    airPressure = sqal.Column('airPressure', sqal.Float)
    humidity = sqal.Column('humidity', sqal.Float)
    apparentTemperature = sqal.Column('apparentTemperature', sqal.Float)
    hourlyPrecipitationDuration = sqal.Column('hourlyPrecipitationDuration', sqal.Float)
    hourlyPrecipitationAmount = sqal.Column('hourlyPrecipitationAmount', sqal.String)
    precipitationProbability = sqal.Column('precipitationProbability', sqal.Float)

    def __init__(self,
                 date,
                 provider,
                 xcoord,
                 ycoord,
                 forecastdelta,
                 temperature,
                 windGustsKmh,
                 airPressure,
                 humidity,
                 apparentTemperature,
                 hourlyPrecipitationDuration,
                 hourlyPrecipitationAmount,
                 precipitationProbability):
        self.date = date
        self.provider = provider
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.forecastdelta = forecastdelta
        self.temperature = temperature
        self.windGustsKmh = windGustsKmh
        self.airPressure = airPressure
        self.humidity = humidity
        self.apparentTemperature = apparentTemperature
        self.hourlyPrecipitationDuration = hourlyPrecipitationDuration
        self.hourlyPrecipitationAmount = hourlyPrecipitationAmount
        self.precipitationProbability = precipitationProbability
        self.hash = time.time()
        print(self.hash, self.forecastdelta)

    def __repr__(self):

        return f"{self.date}"
    @staticmethod
    def Init(engine):
        base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    engine = sqal.create_engine("sqlite:///res//mydb.db", echo=True)
    base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    person = forecast()
    session.add(person)
    session.commit()