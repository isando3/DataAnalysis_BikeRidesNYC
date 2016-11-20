# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 22:46:35 2016

@author: isando3

"""

import math 
import pandas as pd
import numpy as np
import os
from pandas import DataFrame
import utils 

#arrays that contain relevant info for each month of rides
mus_trip_time = []
mus_trip_dist = []
Bad_users = []
Total_users = []
same_spot = []
bike_df = []
BikeDF = DataFrame()

#loop thru each month trip data 
for f in os.listdir("./2015-citibike-tripdata"):
    if f.endswith(".csv"):
        print f
        mu_trip_time, samespot, mu_trip_dist,bad_users, total_users, bikedf = utils.analyze_data("./2015-citibike-tripdata/"+f)
        mus_trip_time.append(mu_trip_time)
        mus_trip_dist.append(mu_trip_dist)
        Bad_users.append(bad_users)
        Total_users.append(total_users)
        same_spot.append(samespot)
        bike_df.append(bikedf)
#data frame to find the number of stations visited by a bike in a year         
BikeDF = pd.concat(bike_df)
BikeDF['counters']=np.repeat(1,len(BikeDF))
#remove those entries where the station has been visited 
BikeDF_clean = BikeDF.drop_duplicates(subset=['bikeid','start station id','end station id'])
#summarize the information
sumBike = BikeDF_clean.groupby(['bikeid']).sum()
max_mean_trip = np.max(mus_trip_time)
min_mean_trip = np.min(mus_trip_time)
delta_means = max_mean_trip - min_mean_trip
fracbadusers = float(np.sum(Bad_users))/float(np.sum(Total_users))
fracsamespot = float(np.sum(samespot))/float(np.sum(Total_users))
print "FINAL RESULTS:"
print "1. Mean duration of a  trip [s]:", np.mean(mus_trip_time)
print "2. Fraction of rides that start  and end at the same station [%]: ", fracsamespot*100
print "3. Std deviation of the number of stations visited by a bike:",sumBike['counters'].std()
print "4. Average lenght of a trip [km]:", np.mean(mus_trip_dist)
print "5a: Average trip duration [s] per month:", mus_trip_time
print "6. Fraction of riders that exceeded their time:", fracbadusers*100
