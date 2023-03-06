import requests
from bs4 import BeautifulSoup
# parses latest temperature in muc from wetteronline
res = requests.get('https://www.wetteronline.de/wetter/muenchen')
soup = BeautifulSoup(res.content, 'lxml')
temp = soup.find_all('div', attrs={'id':'nowcast-card-temperature'})
temperature = int([t.find_all('div', attrs={'class':'value'}) for t in temp][0][0].contents[0])
print('done')