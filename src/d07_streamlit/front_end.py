#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:34:30 2020

@author: eric
"""
import streamlit as st
import datetime as dt
from pytz import timezone
## DISCLAIMER
st.header("DISCLAIMER")
st.markdown("This project is currently in a testing phase. Please take our recommendation with a grain of salt. We invite you to help us improve our accuracy by answering some questions below.")

## DAYS SINCE LOCKDOWN
#st.header("Days Since Lockdown Began")
#from pandas import to_datetime
#lockdown_days = (dt.datetime.now() - to_datetime("03-23-2020")).days
#st.markdown(str(lockdown_days))



## TITLE
st.title("Is it safe to exercise on the main path of Prospect Park right now?")


## RECOMMENDATION

# Function that displays recommendation
def display_recommendation(model):
    # Obtain the verdict from the most recently updated model
    f = open("../d05_reporting/prediction_"+model,"r")
    
    # Define num_ans, a (string representation) of the numerical verdict
    # 0.0 = safe, 1.0 = unsafe
    num_ans = f.read()
    
    # Find the right text answer and thumbs-up or thumbs-down sign
    from PIL import Image
    
    try:
        if float(num_ans) == 0.0:
            ans = "**SAFE** to exercise on the main path."
            image = Image.open('thumbsup.png')
        elif float(num_ans) == 1.0:
            ans = "**NOT SAFE** to exercise on the main path."
            image = Image.open('thumbsdown.png')
        else:
            ans = "**UNCLEAR** whether it is safe to exercise on the main path."
            image = Image.open('shrug.png')
    except:
        ans = "**UNCLEAR** whether it is safe to exercise on the main path."
        image = Image.open('shrug.png')
        
    st.markdown(ans)
    st.image(image)
    
    # Quick Fix for time warning: 
    #st.markdown("Please Note:  \n 1. This recommendation is for " 
    #            + dt.datetime.now(timezone('US/Eastern')).strftime("%-I:%M %p") + 
    #            ". Please refresh the page for an updated recommendation.  \n 2. Our calculations are intended to produce reliable recommendations for times between 7am and 8pm.")
    st.markdown("**Please Note:**")
    st.markdown(" Our calculations are intended to produce reliable recommendations for times between **7am and 8pm**.")
    return num_ans

# Set model = logistic for final recommendation & display
model=''
num_ans = display_recommendation(model = model)


## CORRECT US IF WE'RE WRONG
# Store response submission timestamp as 'time'
# store corrected label as 'safe'
# Store feedback as 'feedback'

st.header("Correct Us if We're Wrong!")

correct = st.radio('Is our recommendation CORRECT?', ('Yes.', 'No.', 'Not sure.'),index=0)
user_input = st.text_input('Feedback / Comments?', value='')
submit = st.button('Submit My Responses')
    
if submit:
    import os
    import sys
    import re
        
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

current_popularity = st.checkbox("current popularity")
if current_popularity:
    #show(current_popularity, 'current_popularity')
    st.markdown("*Coming soon!*")
    
images = st.checkbox("photographs")
if images:
    #show(images, 'images')
    st.markdown("*Coming soon!*")

weather = st.checkbox("weather")
if weather:
    #show(weather, 'weather')
    st.markdown("*Coming soon!*")

geotweets = st.checkbox("geotweets")
if geotweets:
    show(geotweets,'geotweets')
    #st.markdown("*Coming soon!*")

modeling = st.checkbox("model details")
if modeling:
    
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
    st.markdown("*Coming soon!*")

everything = st.checkbox("SHOW ME EVERYTHING")
if everything:
    #show(everything,'')
    st.markdown("*Coming soon!*")


## GITHUB
st.header("Project Code Repository")
st.markdown('[https://github.com/four-insightfellows-corona-project/social_distancing](https://github.com/four-insightfellows-corona-project/social_distancing)')


## SIDEBAR

st.sidebar.title("What Is All This?")
st.sidebar.header("The Inspiration")
st.sidebar.markdown("With COVID-19, social distancing is necessary. But everybody needs fresh air! We wanted to make a tool that Brooklynites could use to identify safe times to exercise in Prospect Park, while observing social distancing.")

st.sidebar.header("Our Data")
st.sidebar.markdown("We gathered weather data, geo-tweets, tweets that tag Prospect Park, photographs of the park, and Google's Popular Times data. From this data we extracted several relevant features that we used to train our model. The tweets and photographs were used for labeling the data only; predictions are made solely based on weather and popular times data.")

st.sidebar.header("The Recommendation")
st.sidebar.markdown("When we give you the \"thumbs up\" to exercise on the main path of Prospect Park, we are saying that by our model's calculations, it is possible to run, walk, or cycle on the main path while maintaining sufficient distance from others to practice social distancing effectively. And for \"thumbs down\", the reverse. Our recommendations are generated by applying a random forest classifier to the weather and Google Popular Times data for the current time period.")
    
st.sidebar.header("How Often?")
st.sidebar.markdown("Our back-end infrastructure collects new data every 15 minutes, and re-trains our model on the updated data once per day.")
    

## RERUN FRONT END EVERY 15MIN AS LONG AS BROWSER IS OPEN
#import time
#from d00_utils.st_rerun import rerun
#time.sleep(900)
#rerun()