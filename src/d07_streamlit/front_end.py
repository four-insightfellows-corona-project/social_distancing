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

# CHOOSE MODEL
st.header("Choose Model")
model = st.radio('How should we calculate our recommendation?', ('logistic regression', 'gradient boosted model'),index=0)

if model == 'logistic regression':
    model = 'logistic'
else: 
    model = 'xgb'

## RECOMMENDATION
st.header("Our Recommendation")
# Obtain the verdict from the most recently updated model
f = open("../d05_reporting/prediction_"+model,"r")
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



## CORRECT US IF WE'RE WRONG
# Store response submission timestamp as 'time'
# store corrected label as 'safe'
# Store feedback as 'feedback'

st.header("Correct Us if We're Wrong!")

correct = st.radio('Is our recommendation CORRECT?', ('Yes.', 'No.', 'Not sure.'),index=0)
user_input = st.text_input('Feedback / Comments?', value='')
submit = st.button('Submit My Responses')
    
if submit:
    import datetime as dt
    from pandas import to_datetime
    from numpy import NaN
    time = to_datetime(dt.datetime.now()) 

    feedback = user_input

    if correct == 'Yes, correct.':
        try:
            safe = int(num_ans)
        except: 
            safe = NaN
            
    elif correct == 'No, incorrect.' :
        try:
            safe = 1-int(num_ans)
        except:
            safe = NaN
    else: 
        safe = NaN


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
    show(modeling,'modeling_'+model)
    f = open("../d05_reporting/modeling_metrics_"+model,'r')
    metrics = f.read()
    st.text(metrics)

everything = st.checkbox("SHOW ME EVERYTHING")
if everything:
    show(everything,'')
