#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 00:11:23 2020

@author: Trey Jiron
"""

import numpy as np
#import qiskit as qc 
#from qiskit import QuantumCircuit, execute, Aer, IBMQ
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt
#from qiskit.visualization import plot_state_city, plot_histogram
import matplotlib.patches as mpatches
from datetime import datetime
from astropy.table import Table
from mpl_toolkits import mplot3d

# function to read the .txt files and convert to list
def read_col(fname, col=1, convert=int, sep=None):
    """Read text files with columns separated by `sep`.

    fname - file name
    col - index of column to read
    convert - function to convert column entry with
    sep - column separator
    If sep is not specified or is None, any
    whitespace string is a separator and empty strings are
    removed from the result.
    """
    with open(fname) as fobj:
         return [convert(line.split(sep=sep)[col]) for line in fobj]

#Makes list for all expectation values
explist = []
Z0explist = []
Z1explist = []
Zexplist = []
Xexplist = []
Yexplist = []
Hexplist = []
invHexplist = []
invHexplisttemp = []
i = 6 # was at 0 for staring at r = 0.2, sets where the r index will start
j = 59 #this means our theta starts at 3 and goes down to -3
thetaindex = np.arange(-3, 3, 0.1) #arrnges theta into list
rindex = np.arange(0.5, 2.85, 0.05) #was starting at 0.2 for i = 0, arranges the r index
g0,g1,g2,g3,g4,g5 = 0.2252, 0.3435, -0.4347, 0.5716, 0.091, 0.091 #sets the constants for our test function

#reads the constants for differnt Rs and puts them into a readable table
tab = Table.read('pea_table_formatted.tex')
arraytab = Table.as_array(tab)
#prints out the table for debugging
print(tab)
print(tab['\openone'][5])

# fills the ex[ecation lists with data from .txt files]
Z0explist = read_col('Zcirc_z0expdata.txt', col=0,convert=float)
Z1explist = read_col('Zcirc_z1expdata.txt', col=0,convert=float)
Zexplist = read_col('Zcirc_z0z1expdata.txt', col=0,convert=float)
Yexplist = read_col('Ycirc_Y0Y1expdata.txt', col=0,convert=float)
Xexplist = read_col('Xcirc_X0X1expdata.txt', col=0,convert=float)

#Calulates H for range of theta and r, exact range is dictate by j and i
while i < 53: 
    while j >= 0:
        #\openone is g0, the constant that is not multiplied by any expecation vaule
        invHexp = (tab['\openone'][i] + Z0explist[j]*tab['$Z_1$'][i] + Z1explist[j]*tab['$Z_0$'][i] 
        + Zexplist[j]*tab['$Z_0Z_1$'][i] + Yexplist[j]*tab['$Y_0 Y_1$'][i] + Xexplist[j]*tab['$X_0 X_1$'][i])
        j -= 1
        invHexplist.append(invHexp)
    i += 1
    j = 59

#resets counters  
j= -3
h = 0

#Caculates the Hamliton expectation value for specific r=0.75 for debugging purposes
while j < 3 :
    invHexptemp = 0.2252 + 0.3435*Z1explist[h] + -0.4317*Z0explist[h] + 0.5716*Zexplist[h] + 0.0910*Xexplist[h] + 0.0910*Yexplist[h]
    invHexplisttemp.append(invHexptemp)
    j += 0.1
    h += 1
    
    
Hexparray = np.reshape(invHexplist, (47, 60)).T #was at 53,60 for r 0.2-2.85 by 0.05, reshaped for graping

#below used to print 3d graph
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
T,R = np.meshgrid(thetaindex, rindex)
ax.plot_surface(T.T, R.T, Hexparray, color='black')
ax.set_title('wireframe');



#plots out expecation values against expectated cos and sin 
plt.figure()   #plots results
plt.plot(thetaindex, Zexplist, 'o')
plt.plot(thetaindex, Z0explist, 'o')
plt.plot(thetaindex, Z1explist, 'o')
plt.plot(thetaindex, Xexplist, 'o')
plt.plot(thetaindex, Yexplist, 'o')
plt.plot(thetaindex, np.cos(thetaindex))
plt.plot(thetaindex, -np.cos(thetaindex))
plt.plot(thetaindex, -np.sin(thetaindex))
orange_patch = mpatches.Patch(color='orange', label='<Z0>') #lables and colors results
blue_patch = mpatches.Patch(color='blue', label='<Z0Z1>')
green_patch = mpatches.Patch(color='green', label='<Z1>')
red_patch = mpatches.Patch(color='red', label = '<X0X1>')
purple_patch = mpatches.Patch(color = 'purple', label = '<Y0Y1>')
brown_patch = mpatches.Patch(color = 'brown', label = 'cos(theta)')
pink_patch = mpatches.Patch(color = 'pink', label = '-cos(theta)')
gray_patch = mpatches.Patch(color = 'gray', label = '-sin(theta)')
plt.legend(handles=[blue_patch, orange_patch, green_patch, red_patch, purple_patch, brown_patch, pink_patch, gray_patch])

#plots H expecation value for r=0.75 and compares to theoreical data.
plt.figure()
plt.plot(thetaindex, invHexplisttemp, 'o')
plt.plot(thetaindex, g0+(g1*-np.cos(thetaindex))+(g2*np.cos(thetaindex))+(-1*g3)+(g4*-np.sin(thetaindex))+(g5*np.sin(thetaindex)))
blue_patch = mpatches.Patch(color='blue', label='experimental data')
orange_patch = mpatches.Patch(color='orange', label='theoretical data')
plt.legend(handles=[blue_patch, orange_patch])

#prints out heatmap for results
#plt.imshow(Hexparray, cmap='hot', interpolation='nearest')
#plt.xticks([0,10,20,30,40,46], [0.5,1.0,1.5,2.0,2.5,2.85])
#plt.yticks([0,10,20,30,40,50,59], [3,2,1,0,-1,-2,-3])
#plt.colorbar()
#plt.show()


