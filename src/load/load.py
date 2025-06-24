from src.utils.common import list_files_from_dir
from src.utils.logger import Logger
import duckdb
import pandas as pd

def prepare_db(db_name):
    conn = duckdb.connect(db_name)
    conn.execute('USE MAIN')
    query = """
        CREATE TABLE IF NOT EXISTS weather_data (
            location TEXT,
            time TIMESTAMP,
            temperature DOUBLE,
            relative_humidity DOUBLE,
            rain DOUBLE,
            snowfall DOUBLE,
            wind_speed DOUBLE,
            surface_pressure DOUBLE,
            cloud_cover DOUBLE,
            is_day INT,
            sunshine_duration DOUBLE,
            PRIMARY KEY (location, time)
        );
    """
    conn.execute(query)
    conn.close()

def load(db_name, logger):
    IMP_DIRNAME = 'data/processed'
    files = list_files_from_dir(IMP_DIRNAME)

    try:
        prepare_db(db_name)
        conn = duckdb.connect(db_name)
        for file in files:
            df = pd.read_csv(file)
            conn.register("df_view", df)
            conn.execute("""
                INSERT INTO weather_data
                SELECT df.*
                FROM df_view df
                LEFT JOIN weather_data wd
                ON df.location = wd.location AND df.time = wd.time
                WHERE wd.location IS NULL
            """)
        conn.close()
        logger.info('Successfuly inserted new records into weather data table.')
    except Exception as e:
        logger.warning(f'Error inserting new records into weather_data table! Error: {e}')

def run_load(db_name):
    logger = Logger('load')
    load(db_name, logger.get_logger())