from src.extract.weather import WeatherAPI
from src.extract.geocoding import GeocodingAPI
from src.extract.extract import extract
from src.transform.transform import transform
from src.utils.logger import Logger
from src.extract.geoextraction import extract_coordinates, process_coordinates

l_w = Logger('weather')
l_g = Logger('geo')
l_t = Logger('transform')
w = WeatherAPI(l_w)
g = GeocodingAPI(l_g)

locations = ['Chisinau', 'Barcelona']

#extract(w, g, locations, '2020-02-01', '2020-02-02')
transform(l_t.get_logger())