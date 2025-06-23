from src.utils.common import list_files_from_dir
import duckdb

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
            conn.execute(f"COPY weather_data FROM '{file}' (AUTO_DETECT TRUE);")
        conn.close()
        logger.info('Successfuly inserted new records into weather data table.')
    except Exception as e:
        logger.warning(f'Error inserting new records into weather_data table! Error: {e}')
