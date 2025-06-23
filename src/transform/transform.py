from src.utils.common import list_files_from_dir, load_json
from src.utils.logger import Logger
import pandas as pd

def process_file(filename, logger):
    data = load_json(filename)
    location = filename.split('_')[0].split('/')[-1].capitalize()
    try:
        results = data['hourly']
        data = {
            'location': [location]*len(results['time']),
            'time': results['time'],
            'temperature': results['temperature_2m'],
            'relative_humidity': results['relative_humidity_2m'],
            'rain': results['rain'],
            'snowfall': results['snowfall'],
            'wind_speed': results['wind_speed_10m'],
            'surface_pressure': results['surface_pressure'],
            'cloud_cover': results['cloud_cover'],
            'is_day': results['is_day'],
            'sunshine_duration': results['sunshine_duration'],
        }
        df = pd.DataFrame(data)
        return df
    except KeyError as e:
        logger.warning(e)

def transform(logger):
    IMP_DIRNAME = 'data/raw/weather'
    EXP_DIRNAME = 'data/processed/'

    files = list_files_from_dir(IMP_DIRNAME)
    for file in files:
        df = process_file(file, logger)
        filename = file.split('/')[-1].split('.')[0] + '.csv'
        df.to_csv(EXP_DIRNAME + filename, index=False)
    logger.info(f'All files from {IMP_DIRNAME} were transformed!')
    