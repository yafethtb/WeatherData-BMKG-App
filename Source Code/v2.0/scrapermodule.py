from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup as bs

@dataclass
class ResponseResult:
    response: requests.Response
    status_code: int

@dataclass
class ConnError:
    error_type: requests.exceptions.ConnectionError
    problem: str

@dataclass
class Weatherdata:
    date: str
    hour: str
    temperature: str
    weather: str
    humidity: str
    wind_speed: str


class BMKGScraper:
    """"Scraping data from BMKG website"""
    def __init__(self, params, tag) -> None:
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
        self.tag = tag
        self.URL = 'https://www.bmkg.go.id/cuaca/prakiraan-cuaca.bmkg' 
        self.session = requests.Session()
    
    @property
    def connection(self):
        """Connect to BMKG website"""    
        try:
            response =  self.session.get(self.URL, params = self.params, headers = self.header)    
            code = response.status_code
            return ResponseResult(response, code)             
        except requests.exceptions.ConnectionError as e:
            return ConnError(e, 'Connection Error')

    @property
    def scraping(self):
        """Scrape data from BMKG website."""
        scraped_html = self.connection

        if isinstance(scraped_html, ResponseResult):
            response = scraped_html.response
            status = scraped_html.status_code
            if status == 200:
                content = response.content
                soup = bs(content, 'html.parser')
                date = soup.find('a', attrs = {'href': f'#{self.tag}'}).get_text()  
                raw_data = soup.find('div', attrs = {'id': self.tag})
                all_weather = raw_data.find_all('div', attrs = {'class': 'cuaca-flex-child'})

                for weather in all_weather:
                    hours_temp = weather.find_all('h2')
                    hours = (hours_temp[0].text).replace('\xa0', ' ')
                    temp = hours_temp[1].text
                    all_p = weather.find_all('p')
                    clouds = all_p[0].text
                    humid = all_p[1].text
                    wind_strength = (all_p[2].get_text(strip=True, separator=' ')).replace('\xa0', ' ')
                    yield Weatherdata(
                        date = date,
                        hour = hours,
                        temperature = temp,
                        weather = clouds,
                        humidity = humid,
                        wind_speed = wind_strength
                    )
            else:
                yield scraped_html
        elif isinstance(scraped_html, ConnError):
            yield scraped_html
