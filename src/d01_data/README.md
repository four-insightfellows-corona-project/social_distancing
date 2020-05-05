# d01_data READMEs
READMEs for the various data utilities in this directory.

## get_data.py
Run this to pull the latest data from the postgres db. You'll need to install the python package `psycopg2`. You'll probably also need to install `libpq-dev` which is the postgres client libraries.

In order to interact with the database, you need to:
- add your ip address to the allowed inbound list, you can use
https://checkip.amazonaws.com/ to get it then send it to Ed on the channel
- add `database.ini` with the connection parameters to your conf folder,
you can find this on the shared folder.
