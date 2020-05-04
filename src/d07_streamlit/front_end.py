#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:34:30 2020

@author: eric
"""
import streamlit as st

## TITLE
st.title("Prospect Park Social Distancing Project")


## DISCLAIMER
st.header("DISCLAIMER")
st.markdown("This project is currently in a testing phase. Please take our recommendation with a grain of salt. We invite you to help us improve our accuracy by answering some questions below.")


## DAYS SINCE LOCKDOWN
#st.header("Days Since Lockdown Began")
#import datetime as dt
#from pandas import to_datetime
#lockdown_days = (dt.datetime.now() - to_datetime("03-23-2020")).days
#st.markdown(str(lockdown_days))


## RECOMMENDATION

st.header("Our Recommendation")

# Function that displays recommendation
def display_recommendation(model):
    # Obtain the verdict from the most recently updated model
    f = open("../d05_reporting/prediction_"+model,"r")
    
    # Define num_ans, a (string representation) of the numerical verdict
    # 0 = safe, 1 = unsafe
    num_ans = f.read()
    
    # Find the right text answer and thumbs-up or thumbs-down sign
    from PIL import Image
    
    try:
        if int(num_ans) == 0:
            ans = "**SAFE** to work out on the main path."
            image = Image.open('thumbsup.png')
        elif int(num_ans) == 1:
            ans = "**NOT SAFE** to work out on the main path."
            image = Image.open('thumbsdown.png')
        else:
            ans = "**UNCLEAR** whether it is safe to work out on the main path."
            image = Image.open('shrug.png')
    except:
        ans = "**UNCLEAR** whether it is safe to work out on the main path."
        image = Image.open('shrug.png')
        
    st.markdown(ans)
    st.image(image)
    st.markdown("Please note: our calculations are intended to produce reliable recommendations for times between 7am and 8pm.")
    return num_ans

# Set model = logistic for final recommendation & display
model='logistic'
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
    import datetime as dt
        
    # Create variables to store:
    
    # Time response was entered
    ins_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Current model recommendation; dtype = Boolean
    ins_rec = num_ans == 0
    
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
        table='feedback_test',
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
    show(current_popularity, 'current_popularity')
    
images = st.checkbox("photographs")
if images:
    show(images, 'images')

weather = st.checkbox("weather")
if weather:
    show(weather, 'weather')

geotweets = st.checkbox("geotweets")
if geotweets:
    show(geotweets,'geotweets')

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
    show(modeling,'modeling_'+model)
    f = open("../d05_reporting/modeling_metrics_"+model,'r')
    metrics = f.read()
    st.text(metrics)

everything = st.checkbox("SHOW ME EVERYTHING")
if everything:
    show(everything,'')


## RERUN FRONT END EVERY 15MIN AS LONG AS BROWSER IS OPEN
#import time
#from d00_utils.st_rerun import rerun
#time.sleep(900)
#rerun()