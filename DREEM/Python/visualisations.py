"""
Copyright (C) 2022 Technoeconomics of Energy Systems laboratory - University of Piraeus Research Center (TEESlab-UPRC)
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# Import Packages
##################
import os
import csv
from auxiliary import readmat, gettime, getval, getmonths, getdays, gethours, discresult, continresult, cumulresult, getmonthly, noelectrific, toexcel

# Change the working directory
###############################
os.chdir('C:/Users/______/Desktop/DREEM/Results')
#os.chdir('C:/Users/______/_______/DREEM/Results/' + folder)

# Reading Results
##################
#filename = 'SC1GR'
#change filename according to the name of the Scenario under study

filename = 'SC1GR'
res = readmat(filename)

# Get Simulation Time
######################
(ts, tm, th, td) = gettime(res)

# Get Simulation Calendar values
################################
mon = getval(res, 'Calendar.month')
dy = getval(res, 'Calendar.day')
hr = getval(res, 'Calendar.hour')

# List with Month, Day, Hour
############################
hours = gethours(hr)
numhours = len(hours)
months = getmonths(numhours, hr, mon)
days = getdays(numhours, hr, dy)

# Get Simulation Results of interest
####################################
# Example 1
###########
values = getval(res, 'weaDat.weaBus.relHum')
#values = getval(res, 'weaDat.weaBus.TDryBul')
#values = values - 273.15
variable1 = discresult(numhours, hr, values)
# Example 2
###########
values = getval(res, 'Grid.y')
variable2 = continresult(numhours, hr, values)
# Example 3
###########
values = getval(res, 'Grid.y')
variable3 = cumulresult(numhours, hr, values)

# Get Monthly Variable Values
##############################
val = discresult(numhours, hr, values = getval(res, 'weaDat.weaBus.relHum'))
humidity = getmonthly(months, val)
val = discresult(numhours, hr, getval(res, 'weaDat.weaBus.TDryBul')-273.15)
temperature = getmonthly(months, val)
sum(temperature)/12

# Relation between Outdoor Air Temperature - Indoor Air Temperature
####################################################################
To = getmonthly(months, discresult(numhours, hr, getval(res, 'weaDat3.weaBus.TDryBul')-273.15))
#ASHRAE
Tn1 = [0 for i in range(len(To))]
for i in range(len(To)):
    Tn1[i] = (0.31*To[i] + 17.8) + 273.15

#de Dear and Brager
Tn2 = [0 for i in range(len(To))]
for i in range(len(To)):
    Tn2[i] = (0.0003*To[i]*To[i] + 22.2) + 273.15

# Consumption profiles for the current situation in Greece
##########################################################
# Read total energy consumption per hour
#Etotal = continresult(numhours, hr, getval(res, 'Grid.y'))
# Read energy consumption per hour from appliances
#Eapp = continresult(numhours, hr, getval(res, 'appliances.EApp'))
# Read occupancy signal - If heating/cooling is on or off
#Ehvac = continresult(numhours, hr, getval(res, 'hVAC.EHVAC'))
# Read cooling signal - If heating or cooling
#signal = continresult(numhours, hr, getval(res, 'hVAC.CoolSignal'))
#total = noelectrific(Etotal, Eapp, Ehvac, signal)

# Read energy consumption per hour - heating
Etherm = continresult(numhours, hr, getval(res, 'hVAC22_1.EHea.y'))

Eel = [0 for k in range(len(Etherm))]
# Read energy consumption per hour - appliances
Eapp = continresult(numhours, hr, getval(res, 'appliances22_1.EApp'))
# Read energy consumption per hour - cooling
Ecool = continresult(numhours, hr, getval(res, 'hVAC22_1.ECool.y'))

for i in range(len(Eel)):
    Eel[i] = Eapp[i] + Ecool[i]

# Export Results to excel files
###############################
results = {'month': months,
           'day': days,
           'hour': hours,
           #'variable': variable2
           'variable1': Etherm,
           'variable2': Eel
           }
columns = ['month', 'day', 'hour', 'variable1', 'variable2']
toexcel(results,columns)

'''
# Upscale to the National level in Greece
##########################################

averDemHouse = sum(Econs_h)
total1 = 51324861.13431603 # MWh
total2 = 46150551.211508766 # MWh

for i in range(len(Econs_h)-1):
    Econs_h[i] = Econs_h[i]*total1/averDemHouse

for i in range(len(Econs_h)-1):
    Econs_h[i] = Econs_h[i]*total2/averDemHouse

os.chdir('C:/Users/Vassilis Stavrakas/Desktop')
# .csv format
with open('load_forecast.csv', 'w') as csvfile:
    csvfile.write('datetime, Demand_forecast\n')
    for i in range(len(Econs_h)):
        s1 = str(i)
        s2 = str(Econs_h[i])
        csvfile.write(s1 + ',' + s2 + '\n')
    csvfile.close()

# .csv format
with open('load_actual.csv', 'w') as csvfile:
    csvfile.write('datetime, Demand_actual\n')
    for i in range(len(Econs_h)):
        s1 = str(i)
        s2 = str(Econs_h[i])
        csvfile.write(s1 + ',' + s2 + '\n')
    csvfile.close()

t = [0 for k in range(len(v1))]
for i in range(len(t)):
    t[i] = i

# Plotting Results
###################

fig = plt.figure()
plt.plot(t, v1, 'y', label='SC1')
plt.plot(t, v2, 'b', label='SC2')
plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
plt.xlabel('Time [hours]', fontsize=10)
plt.ylabel('Electricity Energy Consumption from the Grid (kWh)', fontsize=10)
plt.show()

'''

values1 = getval(res, 'appliances.EApp')
values2 = getval(res, 'hVAC.EVent.y')
v1 = continresult(numhours, hr, values1)
v2 = continresult(numhours, hr, values2)

dem = [0 for i in range(len(v1))]
for i in range(len(dem)):
        dem[i] = v1[i] + v2[i]/2

# Export Results to excel files
###############################
results = {'month': months,
           'day': days,
           'hour': hours,
           'variable': dem
           }
columns = ['month', 'day', 'hour', 'variable']
toexcel(results,columns)

# .txt format
f1 = open('scenario2.txt', 'w')
for item in Etotal:
    f1.write("%s\n" % item)
#f1.close()
