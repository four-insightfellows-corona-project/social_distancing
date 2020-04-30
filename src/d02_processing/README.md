# S3todf.py

Current populartimes are scraped into an S3 bucket as json files. 
This script runs in EC2 to turn these json files into a curpop_df.csv which contains 3 columns: current_popularity, datetime, time_bin