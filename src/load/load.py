import duckdb

def prepare_db(db_name):
    conn = duckdb.connect(db_name)
    conn.execute('USE MAIN')
    query = """
        CREATE TABLE IF NOT EXISTS weather_data (
            location TEXT,
            time TIMESTAMP,
            temperature DOUBLE,
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

def load(db_name, df, logger):
    conn = duckdb.connect(db_name)
    conn.register('df_view', df)
    conn.execute('INSERT INTO weather_data SELECT * FROM df_view')
    conn.close()
