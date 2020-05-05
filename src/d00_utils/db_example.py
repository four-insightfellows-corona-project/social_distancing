#!/usr/bin/env python3

'''

'''

import os
import sys
import datetime as dt

src_dir = os.path.join(os.getcwd(), '..')
root_dir = os.path.join(os.getcwd(), '..', '..')
sys.path.append(root_dir)
sys.path.append(src_dir)

from d00_utils.db_funcs import insert_user_feedback, db_to_df


def main():
    ''' Example code for inserting data into PostgresQL database '''
    # Feedback time; dtype = Timestamp w/o timezone
    ins_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Current model recommendation; dtype = Boolean
    ins_rec = 'false'

    # User accuracy selection; dtype = Text
    ins_user_rec = 'TEST'

    # User feedback; dtype = Text
    ins_feedback = '''May 4 CHAR TEST2 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ CHAR TEST'''

    ins_newcol = 'ajksdh'

    insert_user_feedback(
        table='feedback_test',
        columns=('rec_time', 'rec', 'user_rec', 'feedback'),
        values=(ins_time, ins_rec, ins_user_rec, ins_feedback),
        ini_section='non-social-parks-db')

    print(db_to_df(table='feedback_test', ini_section='non-social-parks-db'))


if __name__ == "__main__":
    main()
