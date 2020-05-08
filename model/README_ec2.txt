
README


- Model is read in from pkl file rfc_HW.pkl



- Run file run_rfc.py to print out a prediction in output.txt
- run_rfc calls rawdata_convert.py
- rawdata_convert.py reads in files from current_weather.csv and current_popularity.csv



HOW TO RUN:

Set up a cron job to run every 5 minutes:
>> python run_rfc.py


https://www.cumulations.com/blogs/37/How-to-write-Cron-jobs-on-Amazon-Web-ServicesAWS-EC2-server


Run:

sudo service crond start

crontab -e

*/5 * * * * cd /home/ec2-user/social_distancing/model && /home/ec2-user/social_distancing/model/my_app/env/bin/python3 run_rfc.py >> ~/cron_logs/logs 2>&1