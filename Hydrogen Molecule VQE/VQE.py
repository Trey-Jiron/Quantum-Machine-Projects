# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 00:23:12 2020

@author: Trey Jiron
"""



import numpy as np
import qiskit as qc 
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.tools.monitor import job_monitor
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt
from qiskit.visualization import plot_state_city, plot_histogram
import matplotlib.patches as mpatches
from datetime import datetime

#IBM backend stuff, provides list of providers and backends for providers, to check what machines you have
#acess to
IBMQ.load_account() # Load account from disk
print(IBMQ.providers()) #list of providers
provider = IBMQ.get_provider(group='colorado-1')   # declares your provider
print('\n')
print(provider.backends()) #list of backends that your provider have access to.

thetaintial = -3 #declares where your theta is going to begin
thetafinal = 3 #where theta ends
thetastep = 0.1 #distance between each theta
runs = 1000 #amount of shots that the machine will run
j = -3 #counter for debug graph
h = 0 #counter for debug graph
thetaindex = np.arange(thetaintial, thetafinal, thetastep).tolist() # aragnes the list of thetas
sinthetaindex = 2*thetaindex # list of theta used for the sin line
# list of all the expectation vaules for the various factors and the hamiltonian
Zexplist = []
Z0explist = []
Z1explist = []
Xexplist = []
Yexplist = []
Hexplist = []
invHexplist = [] #List of Hamiltonian from smallest to largest theta

# Circuit for the Z circuit
def Zcirc(angle) :
    Zcirc = qc.QuantumCircuit(2,2)

    Zcirc.iden(0)
    Zcirc.x(1)
    Zcirc.ry(-1*angle, 0)
    Zcirc.cx(0,1)
    Zcirc.measure([0,1], [0,1])
    return(Zcirc)

# Circuit for the X circuit
def Xcirc(angle) :
    Xcirc = qc.QuantumCircuit(2,2)

    Xcirc.iden(0)
    Xcirc.x(1)
    Xcirc.ry(-1*angle, 0)
    Xcirc.cx(0,1)
    Xcirc.ry(np.pi/2, 0)
    Xcirc.ry(np.pi/2,1)
    Xcirc.measure([0,1], [0,1])
    return(Xcirc)

# Circuit for the Y circuit
def Ycirc(angle) :
    Ycirc = qc.QuantumCircuit(2,2)

    Ycirc.iden(0)
    Ycirc.x(1)
    Ycirc.ry(-1*angle, 0)
    Ycirc.cx(0,1)
    Ycirc.ry(np.pi/2, 0)
    Ycirc.ry(np.pi/2,1)
    Ycirc.measure([0,1], [0,1])
    return(Ycirc)
 
    
#Function to run the Z circuit
#ibmq_vigo was used before for real world results
def Zcircrun() : 
    i = thetaintial
    circname = "Zcircuit"
    while i < 3:
        Zcricreal = Zcirc(i)
        i += 0.1
        backend = provider.get_backend('ibmq_qasm_simulator') #which backend to use
        job = execute(Zcricreal, backend, shots=runs)
        job_monitor(job)
        result = job.result()
        Zcounts = result.get_counts(Zcricreal)
        #print("\nTotal count for 00 and 11 are:",Zcounts) used for debugging
        #plot_histogram(Zcounts) used for debugging
        Zexp = (Zcounts.setdefault('00', 0)/runs) * 1  +  (Zcounts.setdefault('01', 0)/runs) * -1 + (Zcounts.setdefault('10', 0)/runs) * -1 + (Zcounts.setdefault('11', 0)/runs) * 1 
        Z0exp = (Zcounts.setdefault('00', 0)/runs) * 1  +  (Zcounts.setdefault('01', 0)/runs) * -1 + (Zcounts.setdefault('10', 0)/runs) * 1 + (Zcounts.setdefault('11', 0)/runs) * -1 
        Z1exp = (Zcounts.setdefault('00', 0)/runs) * 1  +  (Zcounts.setdefault('01', 0)/runs) * 1 + (Zcounts.setdefault('10', 0)/runs) * -1 + (Zcounts.setdefault('11', 0)/runs) * -1 
        Zexplist.append(Zexp)
        Z0explist.append(Z0exp)
        Z1explist.append(Z1exp)
        #Below printsout info for debugging
        print(circname)
        print(i)
        print(datetime.now().time())
        print(result, '\n')
        
# same as the Z circuit        
def Ycircrun() : 
    i = thetaintial
    circname = "Ycircuit"
    while i < 3:
        Ycircreal = Ycirc(i)
        i += 0.1
        backend = provider.get_backend('ibmq_qasm_simulator')
        job = execute(Ycircreal, backend, shots=runs)
        job_monitor(job)
        result = job.result()
        Ycounts = result.get_counts(Ycircreal)
        #print("\nTotal count for 00 and 11 are:",Zcounts)
        #plot_histogram(Zcounts)
        Yexp = (Ycounts.setdefault('00', 0)/runs) * 1  +  (Ycounts.setdefault('01', 0)/runs) * -1 + (Ycounts.setdefault('10', 0)/runs) * -1 + (Ycounts.setdefault('11', 0)/runs) * 1 
        Yexplist.append(Yexp)
        print(circname)
        print(i)
        print(datetime.now().time())
        print(result, '\n')
#Same as Z circuit
def Xcircrun() : 
    i = thetaintial
    circname = "Xcircuit"
    while i < 3:
        Xcricreal = Xcirc(i)
        i += 0.1
        backend = provider.get_backend('ibmq_qasm_simulator')
        job = execute(Xcricreal, backend, shots=runs)
        job_monitor(job)
        result = job.result()
        Xcounts = result.get_counts(Xcricreal)
        #print("\nTotal count for 00 and 11 are:",Zcounts)
        #plot_histogram(Zcounts)
        Xexp = (Xcounts.setdefault('00', 0)/runs) * 1  +  (Xcounts.setdefault('01', 0)/runs) * -1 + (Xcounts.setdefault('10', 0)/runs) * -1 + (Xcounts.setdefault('11', 0)/runs) * 1 
        Xexplist.append(Xexp)
        print(circname)
        print(i)
        print(datetime.now().time())
        print(result, '\n')
        

        

# Runs the actual code, sends it to the quantum computer and gets date back
Zcircrun()
Xcircrun()
Ycircrun()
        
        
# Plots all the expectation vaules and compares them to cos line.       
plt.plot(thetaindex, Zexplist, 'o')
plt.plot(thetaindex, Z0explist, 'o')
plt.plot(thetaindex, Z1explist, 'o')
plt.plot(thetaindex, Xexplist, 'o')
plt.plot(thetaindex, Yexplist, 'o')
plt.plot(thetaindex, np.cos(thetaindex))
plt.plot(thetaindex, -np.cos(thetaindex))
orange_patch = mpatches.Patch(color='orange', label='<Z0>') #lables and colors results
blue_patch = mpatches.Patch(color='blue', label='<Z0Z1>')
green_patch = mpatches.Patch(color='green', label='<Z1>')
red_patch = mpatches.Patch(color='red', label = '<X0X1>')
purple_patch = mpatches.Patch(color = 'purple', label = '<Y0Y1>')
brown_patch = mpatches.Patch(color = 'brown', label = 'cos(theta)')
pink_patch = mpatches.Patch(color = 'pink', label = '-cos(theta)')
plt.legend(handles=[blue_patch, orange_patch, green_patch, red_patch, purple_patch, brown_patch, pink_patch])


# Prints the circuits out for debugging
print(Zcirc(np.pi).draw())
print(Xcirc(np.pi).draw())
print(Ycirc(np.pi).draw())

#Calcualtes the expectation vaule for the Hamiltonian for specifc r = 0.75 angstroms
while j < 3 :
    Hexp = 0.2252 + 0.3435*Z0explist[h] + -0.4317*Z1explist[h] + 0.5716*Zexplist[h] + 0.0910*Xexplist[h] + 0.0910*Yexplist[h]
    Hexplist.append(Hexp)
    j += 0.1
    h += 1
# resets counters
j= -3
h = 0

# used as above that sets for the Inverse hamilitonian from smallest to biggest theta
while j < 3 :
    invHexp = 0.2252 + 0.3435*Z1explist[h] + -0.4317*Z0explist[h] + 0.5716*Zexplist[h] + 0.0910*Xexplist[h] + 0.0910*Yexplist[h]
    invHexplist.append(invHexp)
    j += 0.1
    h += 1

#plots the hamiltonian expectation value     
plt.figure()
plt.plot(thetaindex, invHexplist, 'o')


#writes all data to text files 
with open('AltZcirc_z0expdata.txt', 'w') as filehandle:
    for listitem in Z0explist:
        filehandle.write('%s\n' % listitem)

with open('AltZcirc_z1expdata.txt', 'w') as filehandle:
    for listitem in Z1explist:
        filehandle.write('%s\n' % listitem) 

with open('AltZcirc_z0z1expdata.txt', 'w') as filehandle:
    for listitem in Zexplist:
        filehandle.write('%s\n' % listitem)

with open('AltYcirc_Y0Y1expdata.txt', 'w') as filehandle:
    for listitem in Yexplist:
        filehandle.write('%s\n' % listitem)
        
with open('AltXcirc_X0X1expdata.txt', 'w') as filehandle:
    for listitem in Xexplist:
        filehandle.write('%s\n' % listitem)

with open('Hexplist.txt', 'w') as filehandle:
    for listitem in Hexplist:
        filehandle.write('%s\n' % listitem) 

with open('invHexplist.txt', 'w') as filehandle:
    for listitem in invHexplist:
        filehandle.write('%s\n' % listitem) 
