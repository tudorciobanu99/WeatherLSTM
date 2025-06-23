import requests
from src.utils.logger import Logger

class WeatherAPI:
    def __init__(self, logger:Logger):
        self.BASE_URL = 'https://archive-api.open-meteo.com/v1/archive'
        self.logger = logger.get_logger()
    
    def get_endpoint(self, **params):
        url = f'{self.BASE_URL}?' \
            + '&'.join([f'{key}={value}' for key, value in params.items()])
        return url

    def prepare_params(self, latitude, longitude, elevation, timezone, start_date, end_date):
        quantities = ["temperature_2m", "relative_humidity_2m", "dew_point_2m", 
                      "apparent_temperature", "precipitation", "rain", 
                      "snowfall", "snow_depth", "wind_speed_10m", 
                      "wind_speed_100m", "wind_direction_10m", "wind_direction_100m", 
                      "wind_gusts_10m", "weather_code", "pressure_msl", 
                      "surface_pressure", "cloud_cover", "cloud_cover_low", 
                      "cloud_cover_mid", "cloud_cover_high", "et0_fao_evapotranspiration", 
                      "vapour_pressure_deficit", "soil_temperature_0_to_7cm", "soil_temperature_7_to_28cm", 
                      "soil_temperature_28_to_100cm", "soil_temperature_100_to_255cm", "soil_moisture_0_to_7cm", 
                      "soil_moisture_7_to_28cm", "soil_moisture_28_to_100cm", "soil_moisture_100_to_255cm", 
                      "boundary_layer_height", "wet_bulb_temperature_2m", "total_column_integrated_water_vapour", 
                      "is_day", "sunshine_duration", "shortwave_radiation", 
                      "direct_radiation", "diffuse_radiation", "global_tilted_irradiance", 
                      "direct_normal_irradiance", "terrestrial_radiation", "shortwave_radiation_instant", 
                      "direct_radiation_instant", "diffuse_radiation_instant", "direct_normal_irradiance_instant", 
                      "global_tilted_irradiance_instant", "terrestrial_radiation_instant"]
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date,
            'end_date': end_date,
            'hourly': ','.join(quantities),
            'timezone': timezone,
            'elevation': elevation,
        }
        return params
    
    def send_request(self, latitude, longitude, elevation, timezone, start_date, end_date):
        params = self.prepare_params(latitude, longitude, elevation, timezone, start_date, end_date)
        url = self.get_endpoint(**params)

        try:
            response = requests.get(url, timeout=10)
            return response
        except requests.exceptions.RequestException as e:
            self.logger.warning(f'Request failed for ({latitude}, {longitude}) on ({start_date}, {end_date}): {e}')

    def get_response(self, response):
        try:
            data = response.json()
            code = response.status_code

            self.logger.info(f'Response was received with status code: {code}.')
            return data
        except requests.exceptions.JSONDecodeError:
            self.logger.warning(response.text)
            return response.text
