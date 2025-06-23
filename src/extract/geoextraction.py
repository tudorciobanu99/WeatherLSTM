from src.extract.weather import WeatherAPI
from src.extract.geocoding import GeocodingAPI
from src.utils.common import save_json, list_files_from_dir, load_json

def extract_coordinates(g:GeocodingAPI, location):
    IMP_DIRNAME = 'data/raw/locations'

    try:
        response = g.send_request(location)
        data = g.get_response(response)

        if data:
            filename = f'{location.lower()}.json'
            save_json(data, IMP_DIRNAME, filename)
            g.logger.info(f'Coordinates for {location} has been extracted successfully.')

    except Exception:
        g.logger.warning(f'Coordinates for {location} have failed extraction!')

def process_coordinates(g:GeocodingAPI, location):
    IMP_DIRNAME = 'data/raw/locations'
    files = list_files_from_dir(IMP_DIRNAME)

    if all(location.lower() not in file for file in files):
        extract_coordinates(g, location)
    else:
        g.logger.info(f'Coordinates for {location} have already been extracted.')

    path = IMP_DIRNAME + f'/{location.lower()}.json'
    data = load_json(path)
    try:
        results = data['results'][0]
        latitude = results['latitude']
        longitude = results['longitude']
        elevation = results['elevation']
        timezone = results['timezone']
        return (latitude, longitude, elevation, timezone)
    except KeyError as e:
        g.logger.warning(e)
