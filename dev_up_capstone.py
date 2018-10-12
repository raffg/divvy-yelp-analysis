
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np
import json
import geopy.distance
# import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')


# # Using Divvy data

# ## Load and concat the Divvy datasets

# In[2]:


# divvy1 = pd.read_csv('data/Divvy_Trips_2017_Q1Q2/Divvy_Trips_2017_Q1.csv', parse_dates=['start_time', 'end_time'])
# divvy2 = pd.read_csv('data/Divvy_Trips_2017_Q1Q2/Divvy_Trips_2017_Q2.csv', parse_dates=['start_time', 'end_time'])
# divvy3 = pd.read_csv('data/Divvy_Trips_2017_Q3Q4/Divvy_Trips_2017_Q3.csv', parse_dates=['start_time', 'end_time'])
# divvy4 = pd.read_csv('data/Divvy_Trips_2017_Q3Q4/Divvy_Trips_2017_Q4.csv', parse_dates=['start_time', 'end_time'])

# divvy = pd.concat([divvy1, divvy2, divvy3, divvy4], ignore_index=True)

# divvy.to_csv('data/divvy_2017.csv')


# In[3]:


divvy = pd.read_csv('data/divvy_2017.csv')


# In[4]:


print(divvy)


# In[5]:


station_list = set(list(divvy['from_station_name'].unique()) + list(divvy['to_station_name'].unique()))
# station_list


# In[6]:


# len(station_list)


# ## Load Divvy station info for GPS coordinates

# In[13]:


with open('data/stations.json') as json_data:
    station_data = json.load(json_data)


# In[14]:


# station_data['stationBeanList']


# In[15]:


stations = [station['stationName'] for station in station_data['stationBeanList']]
latitude = [station['latitude'] for station in station_data['stationBeanList']]
longitude = [station['longitude'] for station in station_data['stationBeanList']]


# In[16]:


# len(stations)


# In[17]:


unknown = []
for station in station_list:
    if station not in stations:
        unknown.append(station)
# unknown


# In[18]:


station_gps = pd.DataFrame({'station_name': stations, 'latitude': latitude, 'longitude': longitude})


# In[19]:


# station_gps.head()


# In[20]:


def gps_lookup(location):
    print(location)
    match = (station_gps['station_name'] == location)
    coord = station_gps['latitude'][match]
    if len(coord) > 0:
        return pd.Series([coord.values[0], station_gps['longitude'][match].values[0]])
    else:
        return pd.Series([np.nan, np.nan])


# In[ ]:


divvy[['from_station_latitude', 'from_station_longitude']] = divvy['from_station_name'].apply(gps_lookup)
divvy[['to_station_latitude', 'to_station_longitude']] = divvy['to_station_name'].apply(gps_lookup)


# In[ ]:


# divvy


# In[ ]:


divvy.to_csv('data/divvy_2017_gps.csv')


# ### 1) Top 5 stations with the most starts (showing # of starts)

# In[ ]:


# station_starts = divvy.groupby(['from_station_name'])['from_station_name'].count().sort_values(ascending=False)
# station_starts.head()


# # In[ ]:


# ax = station_starts.head(5).plot(kind='bar', figsize=(15, 10), title='Top 5 Stations with Most Starts')
# for p in ax.patches:
#     ax.annotate(str(p.get_height()), (p.get_x() * 1.005 + .15, p.get_height() * 1.005))


# # ### 2) Trip duration by user type

# # In[ ]:


# trip_duration = divvy.groupby(['usertype'])['tripduration'].mean().sort_values(ascending=False)
# trip_duration


# # In[ ]:


# ax = divvy.boxplot(column='tripduration', by='usertype', figsize=(15,10))


# # In[ ]:


# ax = divvy.boxplot(column='tripduration', by='usertype', figsize=(15,10), showfliers=False)


# # ### 3) Most popular trips based on start station and stop station

# # In[ ]:


# divvy['trip_stations'] = divvy['from_station_name'] + ' TO ' + divvy['to_station_name']


# # In[ ]:


# trip_stations = divvy.groupby(['trip_stations'])['trip_stations'].count().sort_values(ascending=False)
# trip_stations.head()


# # In[ ]:


# ax = trip_stations.head(10).plot(kind='bar', figsize=(15, 10), title='Top 10 Most Popular Trips')
# for p in ax.patches:
#     ax.annotate(str(p.get_height()), (p.get_x() * 1.005 + .05, p.get_height() * 1.005))


# # ### 4) Rider performance by Gender and Age based on avg trip distance (station to station), median speed (distance traveled / trip duration)

# # Multiply geodesic distance by 1.25. Routes follow roads but the calculated route is direct (geodesic). A route straight down a road would be the same as the direct route; a route diagnoal to roads would be multiplied by 1.414 (thanks, Pythagoras!); assuming routes are evenly split between diagonal and direct, with some wiggle room, I'm splitting the difference at 1.25.
# # 
# # I looked at using the Google Maps api to calculate the actual, along-the-road distance, but they've removed the free api key option. I also looked at Bing Maps, but it's rate limited and I have more than 98,000 routes in this dataset (and once I saw how big that number was, I realized that using api calls would take more than a few days!). So I opted for this *x1.25* method which is less accurate but far quicker and cheaper.

# # In[ ]:


# divvy['trip_distance'] = (1.25 *
#                           geopy.distance.distance((divvy['from_station_latitude'], divvy['from_station_longitude']),
#                                                   (divvy['to_station_latitude'], divvy['to_station_longitude'])).m)


# # # Using Kaggle data

# # In[ ]:


# divvy = pd.read_csv('data/chicago-divvy-bicycle-sharing-data/data_raw.csv', parse_dates=['starttime', 'stoptime'])


# # In[ ]:


# divvy.head()


# # In[ ]:


# divvy.columns


# # In[ ]:


# divvy = divvy[divvy['starttime'].dt.year == 2013]


# # In[ ]:


# divvy


# # ### 1) Top 5 stations with the most starts (showing # of starts)

# # In[ ]:


# station_starts = divvy.groupby(['from_station_name'])['from_station_name'].count().sort_values(ascending=False)
# station_starts.head()


# # In[ ]:


# ax = station_starts.head(5).plot(kind='bar', figsize=(15, 10), title='Top 5 Stations with Most Starts')
# for p in ax.patches:
#     ax.annotate(str(p.get_height()), (p.get_x() * 1.005 + .15, p.get_height() * 1.005))


# # ### 2) Trip duration by user type

# # In[ ]:


# trip_duration = divvy.groupby(['usertype'])['tripduration'].mean().sort_values(ascending=False)
# trip_duration


# # In[ ]:


# ax = divvy.boxplot(column='tripduration', by='usertype', figsize=(15,10))


# # In[ ]:


# ax = divvy.boxplot(column='tripduration', by='usertype', figsize=(15,10), showfliers=False)


# # ### 3) Most popular trips based on start station and stop station

# # In[ ]:


# divvy['trip_stations'] = divvy['from_station_name'] + ' TO ' + divvy['to_station_name']


# # In[ ]:


# trip_stations = divvy.groupby(['trip_stations'])['trip_stations'].count().sort_values(ascending=False)
# trip_stations.head()


# # In[ ]:


# ax = trip_stations.head(10).plot(kind='bar', figsize=(15, 10), title='Top 10 Most Popular Trips')
# for p in ax.patches:
#     ax.annotate(str(p.get_height()), (p.get_x() * 1.005 + .05, p.get_height() * 1.005))


# # ### 4) Rider performance by Gender and Age based on avg trip distance (station to station), median speed (distance traveled / trip duration)

# # In[ ]:


# divvy['trip_distance'] = geopy.distance.vincenty((divvy['from_station_latitude'], divvy['from_station_longitude']),
#                                                  (divvy['to_station_latitude'], divvy['to_station_longitude'])).m

