#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:34:30 2020

@author: eric
"""
import streamlit as st
import datetime as dt
from pytz import timezone
import re

## DISCLAIMER
st.header("DISCLAIMER")
st.markdown("This project is currently in a testing phase. Please take our recommendation with a grain of salt. We invite you to help us improve our accuracy by answering some questions below.")

## DAYS SINCE LOCKDOWN
#st.header("Days Since Lockdown Began")
#from pandas import to_datetime
#lockdown_days = (dt.datetime.now() - to_datetime("03-23-2020")).days
#st.markdown(str(lockdown_days))



## TITLE
st.title("Is now a good time to go to Prospect Park?")
st.markdown("### **Is it easy to practice social distancing in Prospect Park right now?**")


## RECOMMENDATION

# Function that displays recommendation
def display_recommendation(model):
    from pandas import to_datetime
    
    # Obtain the verdict from the most recently updated model
    f = open("../d05_reporting/prediction_"+model,"r")
    
    # Define num_ans, a (string representation) of the numerical verdict
    # 0.0 = safe, 1.0 = unsafe
    prediction = f.read()
    num_ans = re.search('(\d\.\d)',prediction).group(1)
    timestamp = re.search('(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d) \d\.\d',prediction).group(1)
    timestamp = to_datetime(timestamp,utc=True).tz_convert(tz = 'US/Eastern')
    timestamp = timestamp.strftime('%B %d %Y, at %I:%M %p')
    
    # Find the right text answer and thumbs-up or thumbs-down sign
    from PIL import Image
    
    try:
        if float(num_ans) == 0.0:
            image = Image.open('thumbsup.png')
            
        elif float(num_ans) == 1.0:
            image = Image.open('thumbsdown.png')
        else:
            image = Image.open('thumbsdown.png')
    except:
        image = Image.open('thumbsdown.png')
        
    st.image(image)
    
    st.markdown("*This prediction was generated on " + timestamp + ".*")
    
    # Quick Fix for time warning: 
    #st.markdown("Please Note:  \n 1. This recommendation is for " 
    #            + dt.datetime.now(timezone('US/Eastern')).strftime("%-I:%M %p") + 
    #            ". Please refresh the page for an updated recommendation.  \n 2. Our calculations are intended to produce reliable recommendations for times between 7am and 8pm.")
    st.markdown("**Please Note:** Our calculations are intended to produce reliable recommendations for times between **7am and 8pm**.")
    return num_ans

# Set model = logistic for final recommendation & display
model=''
num_ans = display_recommendation(model = model)


## CORRECT US IF WE'RE WRONG
# Store response submission timestamp as 'time'
# store corrected label as 'safe'
# Store feedback as 'feedback'

st.header("Is our prediction accurate?")

correct = st.radio('', ('Yes.', 'No.', 'Not sure.'),index=0)
user_input = st.text_input('Feedback / Comments?', value='')
submit = st.button('Submit My Responses')
    
if submit:
    import os
    import sys
            
    # Create variables to store:
    
    # Time response was entered
    ins_time = dt.datetime.now(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
    
    # Current model recommendation; dtype = Boolean
    ins_rec = num_ans == 0.0
    
    # User accuracy selection; dtype = Text
    ins_user_rec = correct
    
    # User feedback; dtype = Text
    ins_feedback = re.sub('\'','', user_input)
    
    # Send feedback to back end model
    src_dir = os.path.join(os.getcwd(), '..')
    root_dir = os.path.join(os.getcwd(), '..', '..')
    sys.path.append(root_dir)
    sys.path.append(src_dir)
    
        
    from d00_utils.db_funcs import insert_user_feedback
    
    insert_user_feedback(
        table='feedback',
        values=(ins_time, ins_rec, ins_user_rec, ins_feedback),
        ini_section='non-social-parks-db')
    
    st.markdown("*Thank you for submitting your response! We will incorporate your feedback.*")


## SURVEY
#st.header("Survey")
#st.markdown('[_Click Here_](https://docs.google.com/forms/d/e/1FAIpQLSdlczlOJ0s5eM01-HqQhekwlQlbihiW8yqPtsVQbQqNsyB-JQ/viewform) _to help us collect more data!_')


## RECENT PREDICTIONS
st.header("Recent Predictions")

# @st.cache(suppress_st_warning=True)
from pandas import read_pickle
from pickle import load
from pytz import timezone

# Require sklearn 0.22.1
#import pkg_resources
#pkg_resources.require("sklearn==0.22.1")

# Load our data
df = read_pickle("../d01_data/03_from_SQL_for_frontend_ee.pkl")

# Get just the past 7 days of data
oneweekago = (dt.datetime.now(tz=timezone('US/Eastern')) - dt.timedelta(days=7))
df = df[df.index >= oneweekago]
df = df.drop('datetime',axis=1)

# Import our model
rf = load(open("../d03_modeling/rfc_HW.pkl",'rb'))

X = df[['current_popularity', 'wind_speed', 'temp', 
        'status_good', 'status_maybe', 'status_bad', 
        'dayofweek', 'hour']]
df['prediction'] = rf.predict(X)

st.dataframe(df.iloc[0:5])

# ***generate heatmap of past 7 days***
import seaborn as sns

# Create a heatmap where x axis is day, 
# y axis is time bin, and square color is prediction
df.groupby(df.index.day)
data = df.pivot("")
sns.heatmap(--to-be-filledin--)
st.pyplot((--to-be-filledin--)


## DATA
st.header("Data")

def show(box, boxlabel):
    if box:
        import os
        import re
        from PIL import Image
        for filename in os.listdir("../d06_visuals/"):
            if re.match(boxlabel+'.*\.png', filename):
                image = Image.open('../d06_visuals/' + filename)
                st.image(image,use_column_width=True)

#current_popularity = st.checkbox("current popularity")
#if current_popularity:
    #show(current_popularity, 'current_popularity')
#    st.markdown("*Coming soon!*")
    
#images = st.checkbox("photographs")
#if images:
    #show(images, 'images')
#    st.markdown("*Coming soon!*")

#weather = st.checkbox("weather")
#if weather:
    #show(weather, 'weather')
#    st.markdown("*Coming soon!*")

geotweets = st.checkbox("geotweets")
if geotweets:
    show(geotweets,'geotweets')


st.markdown("*More data categories coming soon!*")

#modeling = st.checkbox("model details")
#if modeling:
    
    # CHOOSE MODEL
    #st.header("Choose Model")
    
    # Reset model to chosen model
    #model = st.radio('Which model would you like to explore?', ('logistic regression','random forest','gradient boosted model'),index=0)
    
    #if model == 'logistic regression':
    #    model = 'logistic'
    #elif model == 'random forest': 
    #    model = 'rf'
    #else: 
    #    model = 'xgb'
        
    # Display model results
    #display_recommendation(model)
    
    # Display other model info
    #show(modeling,'modeling_'+model)
    #f = open("../d05_reporting/modeling_metrics_"+model,'r')
    #metrics = f.read()
    #st.text(metrics)
    #st.markdown("*Coming soon!*")

#everything = st.checkbox("SHOW ME EVERYTHING")
#if everything:
    #show(everything,'')
    #st.markdown("*Coming soon!*")


## SIDEBAR

# To make text a different color & style:
# NOTE: Does not seem to work for adjusting font size or weight (bold vs normal),
# can be used for italicizing
# Color options here:  http://www.colors.commutercreative.com/grid/
# st.sidebar.markdown('<style>h4{color:mediumvioletred}</style>', unsafe_allow_html=True)

st.sidebar.title("I want to read more!")
st.sidebar.header("Why social distancing and Prospect Park?")
st.sidebar.markdown("We wanted to make a tool that Brooklynites could use to identify safe times to exercise in Prospect Park, while observing social distancing. [Read more about social distancing.](https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/social-distancing.html)")


st.sidebar.header("What do “thumbs up” and “thumbs down” mean?")
st.sidebar.markdown("When we give you the \"thumbs up\" to exercise on the main path of Prospect Park, we are saying that by our model's calculations, it is possible to run, walk, or cycle on the main path while maintaining sufficient distance from others to practice social distancing effectively. A “thumbs down” means that our model suggests that now is not a good time to exercise in Prospect Park.")

st.sidebar.header("How do you generate the recommendation?")
st.sidebar.markdown("Our recommendations are generated by applying a random forest classifier to data gathered from March 23, 2020 onward. We gathered weather data, geo-tagged tweets and tweet content, photographs of the park, Google's Popular Times data, and survey responses from running clubs and social media sites. From this data we extracted several relevant features that we used to train candidate machine learning models. Survey responses, tweets and photographs were used to create labels; predictions are made on weather, time and popular times data variables. The model is hosted on AWS.")
    
st.sidebar.header("How often does the recommendation update?")
st.sidebar.markdown("Our back-end infrastructure collects new data every 15 minutes, and re-trains our model on the updated data once per day.")

## GITHUB
st.sidebar.header("Can I see your code?")
st.sidebar.markdown('[github repo](https://github.com/four-insightfellows-corona-project/social_distancing)')    

## RERUN FRONT END EVERY 15MIN AS LONG AS BROWSER IS OPEN
#import time
#from d00_utils.st_rerun import rerun
#time.sleep(900)
#rerun()