'''
    Functions built by Huayi to bin pandas dataframes
'''

from datetime import timedelta


def binMinute(minute):
    '''
    Calculate which of the 15min bins the current minute falls in.
    The bins are 05, 20, 35, 50.
    Current minutes less than 05 belong to bin 50 of the hour before.
    '''
    m2q = (minute - 5) / 15
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
    return newminute


def BinTime(df_datetime_col):
    '''
    Take a df column that contains datetime object (df_datetime_col)
    Return a new column that contains the binned datetime object
    The bins are as defined in binMinute
    '''
    binned_col = df_datetime_col.apply(
        lambda x: x.replace(minute=0, second=0) + timedelta(minutes=binMinute(x.minute)))

    return binned_col
