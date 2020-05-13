#!/usr/bin/env python3

'''
A command line utility that obtains the names of all tables in the SQL database 
and stores them in a pickle file in d001_data. 

COMMAND LINE USAGE: 
./get_tablenames_in_SQL_database.py
    
'''

import os
import sys

src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)

from d00_utils.db_funcs import db_to_df


def main():
    
    
    db_to_df(sql = 'SELECT table_name FROM information_schema.tables', ini_section='non-social-parks-db').to_pickle(path="../d01_data/SQL_tables")


if __name__ == "__main__":
    main()
