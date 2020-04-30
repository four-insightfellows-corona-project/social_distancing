# d00_utils READMEs
READMEs for the various utilities in this directory.

## db_funcs.py
In order to interact with the database, you need to:
- add to add your ip address to the allowed inbound list, you can use https://checkip.amazonaws.com/ to get it then send it to Ed on the channel
- add `database.ini` with the connection parameters to your conf folder, message
Ed on the channel for more info.

Function `insert_user_feedback` is for adding user feedback from front-end to
back-end database.
Function `db_to_df` returns a pandas dataframe of the full table of interest.
Currently the db has 2 tables, `feedback` and `feedback_test`, try to keep
`feedback` for real data and use `feedback_test` for testing.
