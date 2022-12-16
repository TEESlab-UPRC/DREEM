"""
Created on Fri May 17 19:05:00 2019
@author: Versus
"""
        ###################################################
        #                                                 #
        #  C6M1: Real-time Demand-Response Price Signals  #
        #                                                 #
################################################################################
# This module is part of the DREEM model TEESlab Modeling (TEEM) suite. This   #
# module simulates DR mechanisms that motivate the consumers to respond to     #
# real-time price signals, which are derived through: (i). considering Hourly  #
# Electricity Prices (HEPs) and a Limiting Price (LP), and (ii). a more        #
# “real-world” situation, in which a central planner, that attempts to maximize#
# flexibility value by issuing DR signals, is assumed. This entity learns the  #
# optimal policy that maximizes its revenues through an optimization approach  #
# based on RL theory.                                                          #
################################################################################
# Import Packages  #
####################
import os
import csv
import numpy as np
import pandas as pd
from tqdm import trange
####################
# (i). HEPs & LPs  #
####################
#####################################s
# (ii). a “real-world” situation    #
#####################################
#   Auxiliary functions  #
##########################
def update_q(state, next_state, action, alpha, gamma):
    rsa = r[state, action]
    qsa = q[state, action]
    new_q = qsa + alpha * (rsa + gamma * max(q[next_state, :]) - qsa)
    q[state, action] = new_q
    rn = q[state][q[state] > 0] / np.sum(q[state][q[state] > 0]) # renormalize row to be between 0 and 1
    q[state][q[state] > 0] = rn
    #print(q)
    return r[state, action]
#####################
#    Input Section  #
#                   #
#####################
# Parameters
#############
#averDemHouse1 = 4.18 # MWh
averDemHouse1 = 11.52 # MWh
#averDemHouse2 = 3.75 # MWh
averDemHouse2 = 8.87 # MWh
G1 = 102.52 # euro/MWh -> Energy Selling Price 

# Load Data
############
#1: SMP: euro/MWh
##################
path = ''
#path = 'Enter path for the yearly SMP on an hourly basis'
csv_colmn_nms = ['datetime','SMP']#,'Consumption']
dstates = pd.read_csv(path,names=csv_colmn_nms, header = 1)
SMP = dstates[csv_colmn_nms[1]]

#2: Demand: Wh -> kWh
######################
path = ''
#path = 'Enter path for the yearly load forecast on an hourly basis'
csv_colmn_nms = ['datetime','Demand_forecast']#,'Consumption']
dstates = pd.read_csv(path,names=csv_colmn_nms, header = 1)
Dem = dstates[csv_colmn_nms[1]]

#3: Consumption: Wh -> kWh
###########################
path = ''
#path = ''nter path for the yearly actual demand on an hourly basis''
csv_colmn_nms = ['datetime','Demand_actual']#,'Consumption']
dstates = pd.read_csv(path,names=csv_colmn_nms, header = 1)
Con = dstates[csv_colmn_nms[1]]

# Total Electricity Consumption (MWh) of Households in Greece
##############################################################
total = 0
for i in range(len(Dem)):
    total += Dem[i]

Dem = (averDemHouse1*Dem)/total

total = 0
for i in range(len(Con)):
    total += Con[i]

Con = (averDemHouse2*Con)/total
#######################################
#         Retailer's Condition  1     #
#######################################
# Retailer's profit with no DR
###############################
profitnoDr = 0
for i in range(len(SMP)):
    profitnoDr = profitnoDr + (G1-SMP[i])*Con[i]
######################################
#                                    #
#   Reinforcement Learning Section   #
#                                    #
######################################
# Actions space -  Available actions
#####################################
#actions = ['nosignal', 'signal'] # 2-actions space
actions = ['nosignal', '5%', '10%', '15%', '20%'] # 5-actions space

# Parameters
#############
gamma = 0.8
alpha = 0.8
epsilon = 0.001
n_episodes = 1000000
n_states = len(dstates)
n_actions = len(actions)
random_state = np.random.RandomState(1999)

# Reward Table
###############
r = -np.ones((n_states,n_actions))

# Initialize 1:n-1
for i in range(n_states-1):
    value_s = (G1-SMP[i])*Dem[i]
    value_ns_a = (G1-SMP[i+1])*(Con[i+1] + (Dem[i]-Con[i]))
    value_ns_na = (G1-SMP[i])*Con[i]
    Va = value_ns_a - value_s
    Vnona = value_ns_na - value_s
    if (Va > Vnona):
        #r[i][1] = 100
        #'''
        shifting = Con[i]/Dem[i]
        if (shifting <= 0.8):
            r[i][1] = 0
            r[i][2] = 0
            r[i][3] = 0
            r[i][4] = 100
        elif (shifting <= 0.85):
            r[i][1] = 0
            r[i][2] = 0
            r[i][3] = 100
        elif (shifting <= 0.90):
            r[i][1] = 0
            r[i][2] = 100
        elif (shifting <= 0.95):
            r[i][1] = 100
        else:
            r[i][0] = 0
            r[i][1] = 0
            r[i][2] = 0
            r[i][3] = 0
            r[i][4] = 0
#'''
        temp = Con[i+1]
        Con[i+1]=temp+(Dem[i]-Con[i])
    else:
        r[i][0] = 100

# Initialize n
value_s = (G1-SMP[n_states-1])*Dem[n_states-1]
value_ns_a = (G1-SMP[0])*(Con[0] + (Dem[n_states-1]-Con[n_states-1]))
value_ns_na = (G1-SMP[n_states-1])*Con[n_states-1]
Va = value_ns_a - value_s
Vnona = value_ns_na - value_s
if (Va > Vnona):
    #r[n_states-1][1] = 100
    #'''
    shifting = Con[n_states-1]/Dem[n_states-1]
    if (shifting <= 0.80):
        r[n_states-1][1] = 0
        r[n_states-1][2] = 0
        r[n_states-1][3] = 0
        r[n_states-1][4] = 100
    elif (shifting <= 0.85):
        r[n_states-1][1] = 0
        r[n_states-1][2] = 0
        r[n_states-1][3] = 100
    elif (shifting <= 0.90):
        r[n_states-1][1] = 0
        r[n_states-1][2] = 100
    elif (shifting <= 0.95):
        r[n_states-1][1] = 100
    else:
        r[n_states-1][0] = 0
        r[n_states-1][1] = 0
        r[n_states-1][2] = 0
        r[n_states-1][3] = 0
        r[n_states-1][4] = 0
#'''
    temp = Con[0]
    Con[0]=temp+(Dem[n_states-1]-Con[n_states-1])
else:
    r[n_states-1][0] = 100

'''
for i in range(len(r)):
    print(r[i])
'''

# Q-value Table
################
q = np.zeros_like(r)

#######################################
#        Q Learning Algorithm         #
#######################################
for e in trange(int(n_episodes)):
    #print(e)
    states = list(range(n_states))
    random_state.shuffle(states)
    current_state = states[0]
    goal = False
    while not goal:
        # epsilon greedy
        valid_moves = r[current_state] >= 0
        if random_state.rand() < epsilon:
            actions = np.array(list(range(n_actions)))
            actions = actions[valid_moves == True]
            if type(actions) is int:
                actions = [actions]
            random_state.shuffle(actions)
            action = actions[0]
            next_state = action
        else:
            if np.sum(q[current_state]) > 0:
                action = np.argmax(q[current_state])
            else:
                # Don't allow invalid moves at the start
                # Just take a random move
                actions = np.array(list(range(n_actions)))
                actions = actions[valid_moves == True]
                random_state.shuffle(actions)
                action = actions[0]
            next_state = action
        reward = update_q(current_state, next_state, action,alpha=alpha, gamma=gamma)
        # Goal state has reward 100
        if reward > 1:
            goal = True
            #print("For Episode_%.0f total reward is : %.2f" % (e, reward))
        current_state = next_state
        #print(goal)

# Optimum Policy - Signals
############################
# Initial Actions Space -  Set of Available Actions
####################################################
#actions = ['nosignal', 'signal'] # 2-actions space
actions = ['nosignal', '5%', '10%', '15%', '20%'] # 5-actions space

policy = ["" for i in range(len(q))]
for i in range(len(q)):
    maxa = 0
    for j in range(len(q[i])):
        if q[i][j] >= maxa:
            maxa = q[i][j]
            pos = j
    policy[i] = actions[pos]

sgnls = np.zeros(len(q))
for i in range(len(q)):
    if (q[i][0] == 1):
        sgnls[i] = 0
    else:
        sgnls[i] = 1

loadsh = np.zeros(len(policy))
cnt = 0
for i in range(len(policy)):
    if (policy[i] == '5%'):
        loadsh[i] = 0.05
        cnt = cnt + 0.05
    elif (policy[i] == '10%'):
        loadsh[i] = 0.10
        cnt = cnt + 0.10
    elif (policy[i] == '15%'):
        loadsh[i] = 0.15
        cnt = cnt + 0.15
    elif (policy[i] == '20%'):
        loadsh[i] = 0.20
        cnt = cnt + 0.20
    else:
        loadsh[i] = cnt
        cnt = 0
#######################################
#                                     #
#        Data Post-Processing         #
#                                     #
#######################################
# Exporting Results
####################
# Q-values
os.chdir('C:/Users/Vassilis Stavrakas/Desktop')

f1 = open('R.txt', 'w')
for item in r:
    f1.write("%s\n" % item)
#f1.close()

f2 = open('Q.txt', 'w')
for item in q:
    temp = 100*item
    np.set_printoptions(precision=2)
    f2.write("%s\n" % temp)
#f2.close()

f3 = open('policy.txt', 'w')
for item in policy:
    f3.write("%s\n" % item)
#f3.close()

os.chdir('C:/Users/Vassilis Stavrakas/Desktop/DREEM/Model/Buildings 5.1.0/Resources/Data/Controls/DemandResponse')

# .csv format
with open('DR_Data.csv', 'w') as csvfile:
    csvfile.write('DATETIME, DR Event\n')
    for i in range(len(q)):
        s1 = str(i)
        s2 = str(sgnls[i])
        s3 = str(loadsh[i])
        csvfile.write(s1 + ',' + s2 + ',' + s3 + '\n')
    csvfile.close()

# .mos format
with open('DR_Data.csv', 'r') as csvfile:
    rea = csv.reader(csvfile, delimiter=',')
    next(rea, None) # Skip header
    tstart = 0
    i = 1
    lines= list()
    for row in rea:
        try:
            lines.append("%.0f, %s, %s\n" % (i*3600+tstart, row[1], row[2]))
            previousRow = row
        except ValueError:
            # Reached the last line, which has again a text
            # At t=0, we used the power of the last interval in the previous year
            l = "%.0f, %s, %s\n" % (0, previousRow[1], previousRow[2])
            lines.insert(0, l)
            pass
        i = i + 1

filOut = open('DR_Data.mos', 'w')
filOut.write("""#1
# The rows in this file are as follows:
#  - time in seconds
#  - demand response signal (0 no demand response, 1 demand response)
#  - load shift during demand response signal
double b90(%s, 3)
""" % len(lines))
filOut.writelines(lines)
filOut.close()

#######################################
#         Retailer's Condition  2     #
#######################################
# Retailer's profit with DR
############################
profitDr = 0
if policy[0] != actions[0]:
    a = (G1-SMP[0])*(Con[0] + (Dem[n_states-1]-Con[n_states-1]))
    profitDr += a
else:
    profitDr += (G1-SMP[n_states-1])*Con[n_states-1]

i = 1
while (i < len(policy)):
    if policy[i] != actions[0]:
        a = (G1-SMP[i])*(Con[i] + (Dem[i-1]-Con[i-1]))
        profitDr += a
    else:
        profitDr += (G1-SMP[i])*Con[i]
    i += 1

print("Retailer's profit: %.2f € or %.2f%%" % ((profitDr-profitnoDr), (100*((profitDr-profitnoDr)/profitnoDr))))

################################################################################

###################################################
    ##### #   #  #####    #####  ##  #   ####
      #   # # #  ###      ###    # # #   #   #
      #   #   #  #####    #####  #  ##   ## #
###################################################
