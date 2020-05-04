#!/usr/bin/env python3

'''

Functions for interacting with the PostgresQL database
Connection parameters are stores in an ini file

'''

import os
import sys
import psycopg2
import pandas as pd
from configparser import RawConfigParser

src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)


def config(filename='database.ini', section='postgresql-local'):
    ''' Reads postgres db connect params from .ini file
    '''
    # create a parser
    parser = RawConfigParser()
    # read config file
    parser.read(os.path.join(root_dir, 'conf', filename))

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db


def insert_user_feedback(
        table='table1',
        columns=('rec_time', 'rec', 'user_rec', 'feedback'),
        values=('2020-04-29 12:20', 'True', 'Default', 'Default'),
        ini_section='postgresql-local'):
    ''' Insert user feedback into PostgresQL db
        -- can't  handle null values as-is
    '''
    cols = (len(columns) - 1) * '{}, '
    vals = '(' + (len(columns) - 1) * '%s, ' + '%s)'

    sql_ins =('INSERT INTO {}(' + cols + ' {})').format(table, *columns)
    sql = sql_ins + '''
    VALUES
          ''' + vals

    conn = None

    try:
        # read connection parameters
        params = config(section=ini_section)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql, values)
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        cur.close()

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def return_query(sql='SELECT * from table', ini_section='postgresql-local'):
    conn = None
    try:
        # read connection parameters
        params = config(section=ini_section)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('Query Output:')
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        cur.close()

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def db_to_df(table='table', ini_section='postgresql-local'):
    conn = None
    try:
        params = config(section=ini_section)

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        sql = 'SELECT * from {}'.format(table)
        df = pd.io.sql.read_sql_query(sql, conn)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return df
