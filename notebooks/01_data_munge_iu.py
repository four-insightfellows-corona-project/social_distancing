


# INPUTS TO SPECIFY:

# Path to data
# Should point to a folder of csv files.
# The script will try to read in all csv files as dataframes.

path = 'alldata/'


# String to specify ind date
end_date = '2020-04-23 23:51:00'



# ----------------- # ----------------- # ----------------- # ----------------- # 



# ----------------- # ----------------- # ----------------- # ----------------- # 
#### READS IN TOOLS

import os
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta 
import seaborn as sns
import re 
from pandas_profiling import ProfileReport
from sklearn.preprocessing import OneHotEncoder
import sklearn

import matplotlib.pyplot as plt

# ----------------- # ----------------- # ----------------- # ----------------- # 

def make_dataframes(path):
    """"""
    file_names = [pos_csv for pos_csv in os.listdir(path) if pos_csv.endswith('.csv')]
    dataframes = {}
    dfs = []
    for i, file in enumerate(file_names):
        df_name = ("df_" + file)[:-4]
        dfs.append(pd.read_csv(path + file))
        dataframes[df_name] = dfs[i]
    return dataframes, file_names