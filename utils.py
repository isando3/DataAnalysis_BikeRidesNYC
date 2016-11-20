# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 22:45:48 2016

@author: isando3
"""

import math 
import pandas as pd
import numpy as np
import os
from pandas import DataFrame

def great_arc(lat1, long1, lat2, long2):
#given the latitude and longitude coordinates of the divy statio
# this function finds the approx lenght in km of the ride.
    R_earth = 6356.752
    phi1 = math.radians(90.0 - lat1)
    phi2 = math.radians(90.0 - lat2)
    theta1 = math.radians(long1)
    theta2 = math.radians(long2)
    Lambda = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    return R_earth*math.acos(Lambda)

def analyze_data(filename):
#returns: the mean duration of trip, the number of bikes returned to the same station where they were picked up
#and the users (customers & subscribers) that exceed the time limit 
    df = DataFrame()
    dfclean = DataFrame()
    bikedf = DataFrame()
    df = pd.read_csv(filename, header=0)
    #find mean of trip time 
    mu_trip_time = df['tripduration'].mean()
    #create sub df without the rides that end at the same start divy station
    dfclean = df.drop(df[df['start station id']==df['end station id']].index)
    samespot = dfclean.shape[0]
    # find the start-end distances
    dfclean['Distance'] = dfclean.apply(lambda x: great_arc(x['start station latitude'], x['start station longitude'], x['end station latitude'], x['end station longitude']), axis=1)
    #find the mean start-end distance 
    mu_trip_dist = dfclean['Distance'].mean()
    #find fraction of subscribers and customers that exceeded time 
    df_exc1= df[(df['usertype']=='Subscriber') & (df['tripduration']> 2700)]
    df_exc2= df[(df['usertype']=='Customer') & (df['tripduration']> 1800)]
    #find net overtimed users 
    bad_users = df_exc1.shape[0]+df_exc2.shape[0]
    total_users = df.shape[0]
    bikedf = df[['bikeid','start station id','end station id']]
    del df, dfclean
    return (mu_trip_time, samespot, mu_trip_dist,bad_users,total_users, bikedf)
