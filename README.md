<a href="http://not-so-social-parks.space/"><img src="/visualizations/logo2.png" width="190" title="logo" alt="logo"></a>

# Social Distancing @ Prospect Park, Brooklyn NY

> Predict the current feasibility of exercising in Prospect Park while observing social distancing

> The product: http://not-so-social-parks.space/

> This project was born in the midst of Covid-19, to help Brooklynites identify safe times to work out on the main path of the Prospect Park, between 7am and 8pm 

## Project Rationale 
### Data
- The model makes predictions with features extracted from weather data, Google's Popular Times data and local time 
- To generate labeled data for training our first model, we also collected geo-tagged tweets, photographs of the park, and survey responses from running clubs and social media groups 
- We are constantly collecting user feedback on our predictions through the survey hosted on our front end 

### Model
- The first model was a random forest classifier trained on a small labeled dataset (515 data points) collected between March 23rd and April 26th, 2020 
- Since the release of the first model, we continue to monitor and update its performance with user feedback 

### Pipeline
<img src="/visualizations/pipeline1.png" width="800" title="logo" alt="logo"></a>

## Team

| <a href="https://github.com/edwardlk" target="_blank">**Ed K**</a> |<a href="https://github.com/eric-epstein-5747" target="_blank">**Eric G. Epstein**</a> | <a href="https://github.com/huayicodes" target="_blank">**Huayi Wei**</a> | <a href="https://github.com/iurrutia" target="_blank">**Isabel Urrutia**</a> |
| :---: |:---:| :---:| :---:|
|<a href="https://github.com/edwardlk"><img src="https://avatars1.githubusercontent.com/u/6785562?s=400&u=02a6a63cac32002eca5fc0f690382a06902bc076&v=4" width="180" title="Ed"></a> | <a href="https://github.com/eric-epstein-5747"><img src="https://avatars2.githubusercontent.com/u/48420096?s=400&u=8ac3c3958fb516b3fe32038ff24f148a404b19ce&v=4" width="180" title="Eric"></a>| <a href="https://github.com/huayicodes"><img src="https://avatars3.githubusercontent.com/u/22870735" width="180" title="Huayi"></a> | <a href="https://github.com/iurrutia"><img src="https://avatars0.githubusercontent.com/u/43141422" width="180" title="Isabel"></a> |
