from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup as bs

@dataclass
class ConnError:
    error_type: str
    problem: str

@dataclass
class Weatherdata:
    hour: str
    temperature: str
    weather: str
    humidity: str

class BMKGConnect:
    """Connecting and asessing connection quality to BMKG website"""    
    def __init__(self, params) -> None:
        self.header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Alt-Used': 'www.bmkg.go.id',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'none',
			'Sec-Fetch-User': '?1',
		}        
        self.params = params
        self.URL = 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca.bmkg' 
        self.session = requests.Session()
        self.response = None
    
    @property
    def connection(self):
        """Connect to BMKG website"""    
        try:
            response =  self.session.get(self.URL, params = self.params, headers = self.header)    
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            return ConnError(repr(e), 'Connection Error')
        except requests.exceptions.HTTPError as errhttp:
            return ConnError(repr(errhttp), 'Bad HTTP response')
        else:
            self.response = response
            return self.response

class BMKGScraper:
    """"Scraping data from BMKG website"""
    def __init__(self, params) -> None:
        self.connection = BMKGConnect(params).connection
        self.is_data = True if isinstance(self.connection, requests.Response) else False

    def scraping(self, tag):
        """Scraping data from BMKG website, if the connection result is exist."""
        if self.is_data:
            content = self.connection.content
            soup = bs(content, 'html.parser')
            raw_data = soup.find('div', attrs = {'id': tag})
            all_weather = raw_data.find_all('div', attrs = {'class': 'cuaca-flex-child'})

            for weather in all_weather:
                hours_temp = weather.find_all('h2')
                hours = (hours_temp[0].text).replace('\xa0', ' ')
                temp = hours_temp[1].text
                all_p = weather.find_all('p')
                clouds = all_p[0].text
                humid = all_p[1].text
                
                yield Weatherdata(                    
                    hour = hours,
                    temperature = temp,
                    weather = clouds,
                    humidity = humid,
                )
        else:
            return self.connection
        
    def label_scraping(self, tag: str ) -> str:
        """Scraping tab's label/name"""
        if self.is_data:
            content = self.connection.content
            soup = bs(content, 'html.parser')
            raw = soup.find('a', attrs = {'href': f'#{tag}'})
            return raw.text
        else: 
            return "No Label"
        