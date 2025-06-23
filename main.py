from src.extract.weather import WeatherAPI
from src.extract.geocoding import GeocodingAPI
from src.extract.extract import extract
from src.transform.transform import transform
from src.load.load import load
from src.utils.logger import Logger

l_e = Logger('extract')
l_t = Logger('transform')
l_l = Logger('load')
w = WeatherAPI(l_e)
g = GeocodingAPI(l_e)

locations = ['London', 'Paris', 'Kyiv']

extract(w, g, locations, '2020-02-02', '2020-02-03')
transform(l_t.get_logger())
load('src/database/weather.duckdb', l_l.get_logger())