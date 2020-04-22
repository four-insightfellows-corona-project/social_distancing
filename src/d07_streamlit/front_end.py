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
ans = "**NO.**"
st.markdown(ans)


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


## SURVEY
st.header("Survey")
st.markdown("_Help Us Collect More Data!_")
import webbrowser
url = 'https://docs.google.com/forms/d/e/1FAIpQLSdlczlOJ0s5eM01-HqQhekwlQlbihiW8yqPtsVQbQqNsyB-JQ/viewform'

if st.button('Click Here'):
    webbrowser.open_new_tab(url)

