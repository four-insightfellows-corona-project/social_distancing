
README

Set up a cron job to run every 5 minutes:
>> python run_rfc.py


https://www.cumulations.com/blogs/37/How-to-write-Cron-jobs-on-Amazon-Web-ServicesAWS-EC2-server


Run:

sudo service crond start

crontab -e

*/5 * * * * cd /home/ec2-user/social_distancing/model && /home/ec2-user/social_distancing/model/my_app/env/bin/python3 run_rfc.py >> ~/cron_logs/logs 2>&1