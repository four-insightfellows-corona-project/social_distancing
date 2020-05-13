#!/usr/bin/env python3

'''
Obtains specified table from Ed's SQL database, and 
and deposits in ../d01_data.

COMMAND LINE USAGE: 
./get_table.py 'feedback'
./get_table.py 'weather_test'

'''

import os
import sys

src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)

from d00_utils.db_funcs import db_to_df


def main():
    
    
    table_name = sys.argv[1]
    
    db_to_df(sql = 'SELECT * FROM '+ table_name, ini_section='non-social-parks-db').to_pickle(path = '../d01_data/from_SQL_'+table_name)


if __name__ == "__main__":
    main()
