import boto3
import pandas as pd
from datetime import datetime, timedelta
import json
from io import StringIO

def binMinute(minute):
    '''
    Calculate which of the 15min bins the current minute falls in.
    The bins are 05, 20, 35, 50. 
    Current minutes less than 05 belongs to bin 50 of the hour before. 
    '''    
    m2q= (minute-5)/15
    if m2q < 0:
        newminute = -10 
    elif m2q < 1:
        newminute = 5
    elif m2q < 2:
        newminute = 20
    elif m2q < 3:
        newminute = 35
    elif m2q < 4:
        newminute = 50
    return(newminute)       


if __name__ == '__main__':  
    data = pd.DataFrame()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('pop-time-data')
    idx = 0
    for item in bucket.objects.filter(Prefix = "Data/"):
        content = item.get()['Body'].read().decode('utf-8')
        if len(content):
            json_content = json.loads(content)['current_popularity']
            timestamp = datetime.strptime(item.key[5:-5], '%m%d%Y_%H%M')
            data = data.append(pd.DataFrame({'current_popularity': json_content, 'datetime': timestamp}, index = [idx]))
            idx +=1
     
    # change time zone
    data['datetime'] = data['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern').dt.tz_localize(None)
    # bin the time
    data['time_bin'] = data['datetime'].apply(lambda x: x.replace(minute = 0) + timedelta(minutes=binMinute(x.minute)))
        
    # save to s3 bucket
    csv_buffer = StringIO()
    data.to_csv(csv_buffer) # save to a buffer first
    s3.Object('pop-time-data', 'CSV/curpop_df.csv').put(Body = csv_buffer.getvalue())