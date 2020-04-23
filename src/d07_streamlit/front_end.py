#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:34:30 2020

@author: eric
"""
import streamlit as st

## TITLE
st.title("Prospect Park Social Distancing Project")


## ANSWER
st.header("Is it safe to visit Prospect Park right now?")
f = open("../d05_reporting/prediction_for_most_recent_timebin","r")
num_ans = f.read()

try:
    if int(num_ans) == 0:
        ans = "**YES.**"
    elif int(num_ans) == 1:
        ans = "**NO.**"
    else:
        ans = "**NOT SURE.**"
except:
    ans = "**NOT SURE.**"
    
st.markdown(ans)


## SURVEY
st.header("Survey")
st.markdown('[_Click Here_](https://docs.google.com/forms/d/e/1FAIpQLSdlczlOJ0s5eM01-HqQhekwlQlbihiW8yqPtsVQbQqNsyB-JQ/viewform) _to help us collect more data!_')


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
