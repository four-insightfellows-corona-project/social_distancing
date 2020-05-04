#!/usr/bin/env python3

'''

Functions for interacting with the PostgresQL database
Connection parameters are stores in an ini file

'''

import os
import sys
import psycopg2
import pandas as pd

src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)

from d00_utils.db_funcs import config


def current():
    ''' Pulls the last row of data from the popular times and weather db's.
        Saves the data to csv's & returns the df's.
    '''
    conn = None

    w_sql = 'SELECT * FROM weather_test ORDER BY ID DESC LIMIT 1;'
    t_sql = 'SELECT * FROM popular_times_test ORDER BY ID DESC LIMIT 1;'

    try:
        params = config(section='non-social-parks-db')

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        w_df = pd.io.sql.read_sql_query(w_sql, conn)
        w_df.to_csv(os.path.join(root_dir, 'data', 'current_weather.csv'),
                    index=False)

        t_df = pd.io.sql.read_sql_query(t_sql, conn)
        t_df.to_csv(os.path.join(root_dir, 'data', 'current_popularity.csv'),
                    index=False)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return w_df, t_df


if __name__ == "__main__":
    current()
