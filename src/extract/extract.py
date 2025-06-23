from src.extract.weather import WeatherAPI
from src.extract.geocoding import GeocodingAPI
from src.extract.geoextraction import process_coordinates
from src.utils.common import save_json

def extract(w:WeatherAPI, g:GeocodingAPI, locations, start_date, end_date):
    IMP_DIRNAME = 'data/raw/weather'

    for location in locations:
        try:
            coords = process_coordinates(g, location)
            if coords:
                params = coords + (start_date, end_date)
                response = w.send_request(*params)
                data = w.get_response(response)

                if data:
                    filename = f'{location.lower()}_{start_date}_{end_date}.json'
                    save_json(data, IMP_DIRNAME, filename)
                    w.logger.info(f'Weather data for {location} and ({start_date},{end_date})'
                            + ' has been extracted successfully.')
        except Exception:
            w.logger.warning(f'Weather data for {location} and ({start_date},{end_date})'
                            + ' has failed extraction!')