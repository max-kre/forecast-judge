import json
import requests
from bs4 import BeautifulSoup
import re
import dill
from datetime import datetime as dt
import glob
from ForecastData import ForecastData
import sqlalchemy as sqal
from sqlalchemy.orm import sessionmaker, declarative_base
'''
TODO: 
1. detect double commits to database and handle without error
2. collect data
3. start building a metric to evaluate forecast-goodness
'''
REGEX =  re.compile('\n^(.*?):(.*?)$|,', re.MULTILINE)
TIMESTAMP_FORMAT = "%Y%m%d-%H%M%S"
LOC_TO_COORDS = {'München': (48.1212, 11.5648),}

class ScrapeBase:
    def __init__(self, loc, provider, url):
        self.now = dt.now()
        self.loc = loc
        self.provider = provider
        self.url = url
        self.soup = ''
        self.engine = sqal.create_engine("sqlite:///res//mydb.db", echo=True)
        #self.metadata = sqal.MetaData()
        ForecastData.Init(self.engine)
        #base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()        
        
    @staticmethod
    def getNowStr(dttimestamp=None):
        if dttimestamp:
            return dt.strftime(dttimestamp, TIMESTAMP_FORMAT)
        return dt.strftime(dt.now(), TIMESTAMP_FORMAT)
    
    def locToCoords(self):
        return LOC_TO_COORDS.get(self.loc)
    
    def getData(self, download=True):
        self.now = dt.now()
        if download:
            res = requests.get(self.url, timeout=30)
            with open(f'res\{self.provider}_{self.loc}_{self.getNowStr(self.now)}_page.dill', 'wb') as f:
                dill.dump(res, f)
        files = sorted(glob.glob(f'res\{self.provider}_{self.loc}_*.dill'))
        file = files[-1]
        res = dill.load(open(file,'rb'))
        self.soup = BeautifulSoup(res.content, 'lxml')
    
    def writeToDatabase(self, row:dict, ):
        
        if not row.get('xcoord'):
            xcoord, ycoord = self.locToCoords()
            row['xcoord'] = xcoord
            row['ycoord'] = ycoord
            

        if not row.get('date'):
            row['date'] = self.now
        if not row.get('provider'):
            row['provider'] = self.provider
        forecast = ForecastData(**row)
        self.session.add(forecast)
        self.session.commit()
        
    
class ScrapeWeatherOnline(ScrapeBase):

    def __init__(self):
        self.provider = 'WO'
        self.loc = 'München'
        self.url='https://www.wetteronline.de/wetter/muenchen'
        super().__init__(self.loc, self.provider, self.url)

    def prepareSoup(self):
        #temp = soup.find_all('div', attrs={'id':'nowcast-card-temperature'})
        self.hourlies_soup = self.soup.find_all('div', attrs={'id':'hourly-container'})


    def parseHourlies(self):
        #hourlies = [x.text for x in hourlies_soup[0].find_all('script')]
        hourlies = [re.findall(REGEX, x.text) for x in self.hourlies_soup[0].find_all('script')]
        for hourly in hourlies:
            hdict = self.interestingInfosToDict(hourly)
            
            hdict['provider'] = self.provider
            self.writeToDatabase(hdict)        

    def interestingInfosToDict(self, hourly, interesting=[
                 'hour','date', 'xcoord', 'ycoord', 'forecastdelta', 'temperature', 'windGustsKmh', 'airPressure', 'humidity', 'apparentTemperature', 'hourlyPrecipitationDuration', 'hourlyPrecipitationAmount', 'precipitationProbability'
                ]):
        hdict = {}
        for info in hourly:
            key = info[0].strip()
            val = info[1].strip().replace('"','').replace(',','')
            try: 
                val = float(val)
            except ValueError:
                pass            
            if key in interesting:
                hdict[key] = val
        forecastdelta = (self.now.replace(hour=int(hdict['hour'])) - self.now).seconds/3600
        hdict['forecastdelta'] = forecastdelta
        hdict.pop('hour')
        return hdict

class ScrapeYrNo(ScrapeBase):

    def __init__(self):
        self.provider = 'YrNo'
        self.loc = 'München'
        self.url='https://www.yr.no/en/forecast/daily-table/2-2867714/'
        super().__init__(self.loc, self.provider, self.url)

    def prepareSoup(self):
        scripts = self.soup.find_all('script')
        data = [x.string for x in scripts if x.string and x.string.startswith('\n    window.__LOCALE_CODE__ ')][0]
        data = re.search('window.__REACT_QUERY_STATE__ = JSON.parse(.*)',data)
        if data:
            data = data.group(1)
            data = data[2:-3] # abschneiden von (" am anfang und ") am ende
            data = data.replace('\\"', '"') \
                    .replace('\\\\', '') \
                    .replace('"[', '[') \
                    .replace(']"', ']')
            data = json.loads(data)
        return data or None
    

if __name__ == '__main__':
    scraper = ScrapeYrNo()
    scraper.getData(download=False)
    data = scraper.prepareSoup()
    data
    
    # scraper.prepareSoup()
    # scraper.parseHourlies()

    # temperature = int([t.find_all('div', attrs={'class':'value'}) for t in temp][0][0].contents[0])
    # print(temperature)
    # print('done')


