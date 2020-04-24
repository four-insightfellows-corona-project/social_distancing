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

## RECOMMENDATION
st.header("Our Recommendation")

# Obtain the verdict from the most recently updated model
f = open("../d05_reporting/prediction_for_most_recent_timebin","r")
num_ans = f.read()

# Find the right text answer and thumbs-up or thumbs-down sign
from PIL import Image

try:
    if int(num_ans) == 0:
        ans = "According to our analysis, it is **SAFE** to visit Prospect Park right now."
        image = Image.open('thumbsup.png')
    elif int(num_ans) == 1:
        ans = "According to our analysis, it is **NOT SAFE** to visit Prospect Park right now."
        image = Image.open('thumbsdown.png')
    else:
        ans = "Our analysis is **UNCLEAR** on whether it is safe to visit Prospect Park right now."
        image = Image.open('shrug.png')
except:
    ans = "Our analysis is **UNCLEAR** on whether it is safe to visit Prospect Park right now."
    image = Image.open('shrug.png')
    
st.markdown(ans)
st.image(image)



## HELP US IMPROVE
st.header("Help Us Improve!")

agree = st.checkbox('Click here to answer a few questions that will improve our predictions.')

if agree:
    in_park = st.radio('Are you in Prospect Park right now?', ('Yes', 'No'), index=1)
    if in_park == "Yes":
        activity = st.radio('What activity are you doing?', ('Walking', 'Running','Cycling','Other', 'no answer'), index=4)
        main_track = st.radio('Is it EASY or DIFFICULT to practice social distancing ON the MAIN TRACK of Prospect Park?', ('easy', 'difficult', 'can\'t tell'),index=2)
        not_main_track = st.radio('Is it EASY or DIFFICULT to practice social distancing APART FROM the MAIN TRACK of Prospect Park?', ('easy', 'difficult', 'can\'t tell'),index=2)

    elif in_park == "No":
        activity = st.radio('What activity were you doing?', ('Walking', 'Running','Cycling','Other', 'no answer'), index=4)
        day = st.date_input("What day were you in Prospect Park?")
        time = st.time_input('What time were you in Prospect Park? (24h clock)')
        main_track = st.radio('Was it EASY or DIFFICULT to practice social distancing ON the MAIN TRACK of Prospect Park?', ('easy', 'difficult', 'can\'t tell'),index=2)
        not_main_track = st.radio('Was it EASY or DIFFICULT to practice social distancing APART FROM the MAIN TRACK of Prospect Park?', ('easy', 'difficult', 'can\'t tell'),index=2)


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

validation = st.checkbox("model validation")
if validation:
    show(validation,'validation')

everything = st.checkbox("SHOW ME EVERYTHING")
if everything:
    show(everything,'')
