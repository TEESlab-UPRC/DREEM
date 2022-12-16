"""
Created on Sat Apr 20 14:53:00 2019

@author: Versus
"""
###################################################
#                                                 #
#       Auxiliary functions/Post-Processing       #
#                                                 #
###################################################
#
# Import Packages
##################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from buildingspy.io.outputfile import Reader

# Read .mat file Simulation Results
#######################################
def readmat(filename):
    result = filename + '.mat'
    r = Reader(result, "dymola")
    return r

def gettime(r): #simulation time
    (ts, y) = r.values('Calendar.hour') #simulation time in seconds
    tm = ts/60 #simulation time in minutes
    th = ts/3600 #simulation time in hours
    td = ts/86400 #simulation time in days
    return ts, tm, th, td

def getval(r,var):
    (ts, y) = r.values(var)
    return y

def gethours(hr):
    cnt = 0
    for i in range(len(hr)-1):
        if hr[i] != hr[i+1]:
            cnt += 1
    hours = [0 for k in range(cnt)]
    j = 0
    for i in range(len(hr)-1):
        if hr[i] != hr[i+1]:
            hours[j] = hr[i]
            j += 1
    return hours

def getdays(numhours, hr, dy):
    days = [0 for k in range(numhours)]
    j = 0
    for i in range(len(hr)-1):
        if hr[i] != hr[i+1]:
            days[j] = dy[i]
            j += 1
    return days

def getmonths(numhours, hr, mon):
    months = [0 for k in range(numhours)]
    j = 0
    for i in range(len(hr)-1):
        if hr[i] != hr[i+1]:
            months[j] = mon[i]
            j += 1
    return months

# This function is to read discret values results at each hour, e.g., PMV,
# indoor temperature, outdoor temperature, etc.
def discresult(numhours, hr, values):
    var = [0 for k in range(numhours)]
    j = 0
    for i in range(len(hr)-1):
        if hr[i] != hr[i+1]:
            var[j] = values[i]
            j += 1
    return var

# This function is to read continuous values results during each hour, e.g.,
# electricity consumption profiles, etc.
def continresult(numhours, hr, values):
    var = [0 for k in range(numhours)]
    j = 0
    temp = 0
    for i in range(len(hr)-1):
        if hr[i] != hr[i+1]:
            var[j] = values[i] - temp
            temp += var[j]
            j += 1
    return var

# This function is to read continuous values results cumulatively, e.g.,
# total electricity consumption, etc.
def cumulresult(numhours, hr, values):
    var = [0 for k in range(numhours)]
    j = 0
    for i in range(len(hr)-1):
        if hr[i] != hr[i+1]:
            var[j] = values[i]
            j += 1
    return var

# This function is to derive monthly relative humidity/temperature for the city
# under study
def getmonthly(months, hum):
    value = [0 for k in range(12)]
    for i in range(12):
        cnt = 0
        sum = 0
        for j in range(len(months)):
            if (months[j] == i+1):
                cnt += 1
                sum += hum[j]
        value[i] = sum/cnt
    return value

# This function computes total electricity consumption per hour for the scenario
# that no full electrification of heating/cooling in the residential sector
# is assumed.
# The annual average electrical energy use per household is 3750 kWh, which is
# used for cooling(4.9%) and space heating (3%).
def noelectrific(Etotal, Eapp, Ehvac, signal):
    temp = 0
    total = [0 for k in range(len(Etotal))]
    for i in range(len(Etotal)):
        if (signal[i] == 0):
            fact = 0.030
        else:
            fact = 0.049
        cons = fact * Etotal[i]
        if (Ehvac[i] != 0):
            total[i] = Eapp[i] + cons - temp
            temp = 0
        else:
            total[i] = Eapp[i]
            temp += cons
    return total

def ploting(t,y,ttl,xlab,ylab):
    fig = plt.figure()
    plt.plot(t, y)
    fig.suptitle(ttl, fontsize=12)
    plt.xlabel(xlab, fontsize=10)
    plt.ylabel(ylab, fontsize=10)
    plt.show()

def toexcel(results,columns):
    df = pd.DataFrame(results, columns= columns)
    df.to_excel('plot.xlsx', header=False, index=False)
