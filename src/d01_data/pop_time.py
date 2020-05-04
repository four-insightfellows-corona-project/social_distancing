#!/usr/bin/env python3

'''


'''

import os
import sys
import time
import json
import datetime
import populartimes

src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)

from d00_utils.db_funcs import insert_user_feedback
from conf.auth import google_api

def pop_time():
    '''
    '''
    tz_offset = -14400

    cols = ['local_time', 'place_name', 'current_pop', 'data_json']

    data = populartimes.get_id(google_api, 'ChIJQwRohxBbwokRmHrfAMb3ixc')
    t = time.time() + tz_offset
    data_json = json.dumps(data)

    vals = [
        int(t),
        data['name'],
        data['current_popularity'],
        data_json
    ]

    insert_user_feedback(
        table='popular_times_test',
        columns=cols,
        values=vals,
        ini_section='non-social-parks-db'
    )

if __name__ == '__main__':
    pop_time()
