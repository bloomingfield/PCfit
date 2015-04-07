"""

Nathaniel Bloomfield

14/12/14

This code takes the data reduced .py file and plots histograms with them.
I want the histograms also to show means and standard deviations with a dotted red line, like I did for the equipartition.
Would be great if eventually I could show a number of different temperatures on the same graph.

"""

from __future__ import division
import scipy as sp
import matplotlib
matplotlib.use('tkagg')
import numpy
from numpy import genfromtxt
from copy import deepcopy
import argparse
import csv
from pylab import *

def choose_option():
    loop = False
    while loop == False:
        print 'Would you like to compare conditions or concentrations?'
        print "Press 1 to compare conditions, and 2 to compare concentrations "
        userinput = raw_input('Select the number you wish: ')
        if userinput.isdigit() == True and 0 < int(userinput) < 3:
            Option = int(userinput)
            break
        else:
            print "Invalid input, try again."
            continue
    return Option

parameter = {0 : 'a',
                1 : 'b',
                2 : 'c',
                3 : 'd',
}

def grapher (Option):
    fiddling = CONC_WELLS_CONST[j]
    for k in range(4):
        weight = np.ones_like(fiddling[:,k])/len(fiddling[:,k])
        mu = numpy.mean(fiddling[:,k], axis=0)
        sigma = numpy.std(fiddling[:,k], axis=0)

        if Option == 1:
            plt.figure(str(k)+str(j))
            plt.hist(fiddling[:,k], bins[j][k], alpha=0.5,  label=CONDITIONS , weights = weight)
            plt.suptitle('Fitted '+ parameter[k]+' at wavelength '+str(use_wavelength)+'nm and concentration '+ str(CONCENTRATIONS[j])+CONC_UNIT)
            plt.annotate(CONDITIONS, xy=(mu, 0.0),  xycoords='data',
                xytext=(0, 10*i+50), textcoords='offset points',
                arrowprops=dict( shrink=0.05),
                horizontalalignment='center', verticalalignment='center',
                )
        elif Option == 2:
            plt.figure(CONDITIONS+str(k))
            plt.hist(fiddling[:,k], bins[k], alpha=0.5,  label=str(CONCENTRATIONS[j]) , weights = weight)
            plt.suptitle('Fitted '+ parameter[k]+' at wavelength '+str(use_wavelength)+'nm and concentration '+ str(CONCENTRATIONS[j])+CONC_UNIT)
            plt.annotate(str(CONCENTRATIONS[j]), xy=(mu, 0.0),  xycoords='data',
                xytext=(0, 10*i+50), textcoords='offset points',
                arrowprops=dict( shrink=0.05),
                horizontalalignment='center', verticalalignment='center',
                )


        plt.xlabel('Value of parameter'+ parameter[k])
        plt.ylabel('Frequency')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.draw()
        plt.pause(0.1)

def minMax (Option):
    global datafiles

    with open(datafiles[0]) as f:
        carryData = {}
        code = compile(f.read(), datafiles[0], 'exec')
        exec(code, carryData)

    thisArray = []
    for i in range(size(carryData['CONCENTRATIONS'])):
        thisArray.append([])
        for k in range(4):
            if Option == 'max':
                thisArray[i].append([0])
            elif Option == 'min':
                thisArray[i].append([10000])

    for i in range(size(datafiles)):
        with open(datafiles[i]) as f:
            carryData = {}
            code = compile(f.read(), datafiles[i], 'exec')
            exec(code, carryData)

        for j in range(size(carryData['CONCENTRATIONS'])):
            middleMe = carryData['CONC_WELLS_CONST']
            fiddling = middleMe[j]
            for k in range(4):
                if Option == 'max':
                    tests = numpy.amax(fiddling[:,k])
                    if tests > thisArray[j][k]:
                        thisArray[j][k] = tests
                elif Option == 'min':
                    tests = numpy.amin(fiddling[:,k])
                    if tests < thisArray[j][k]:
                        thisArray[j][k] = tests
    return thisArray


parser = argparse.ArgumentParser()
parser.add_argument('DATA', type=str, nargs='*', help='File path to the reduced data file.')
#should add support for multiple csv files later

parsed = parser.parse_args()   #parses sys.argv by default

Option = choose_option()


#loading config file
datafiles = parsed.DATA

maxs = minMax('max')
mins = minMax('min')

print maxs
print mins
# maxs = []
# for i in range(size(CONCENTRATIONS)):
#     maxs.append([])
#     for k in range(4):
#         maxs[i].append([0])

# for i in range(size(datafiles)):
#     execfile(datafiles[i])
#     for j in range(size(CONCENTRATIONS)):
#         fiddling = CONC_WELLS_CONST[j]
#         for k in range(4):
#             tests = numpy.amax(fiddling[:,k])
#             if tests > maxs[j][k]:
#                 maxs[j][k] = tests

# mins = []
# for i in range(size(CONCENTRATIONS)):
#     mins.append([])
#     for k in range(4):
#         mins[i].append([0])

# for i in range(size(datafiles)):
#     execfile(datafiles[i])
#     for j in range(size(CONCENTRATIONS)):
#         fiddling = CONC_WELLS_CONST[j]
#         for k in range(4):
#             tests = numpy.amin(fiddling[:,k])
#             if tests > mins[j][k]:
#                 mins[j][k] = tests


execfile(datafiles[0])
bins = []
if Option == 1:

    for i in range(size(CONCENTRATIONS)):
        bins.append([])
        for k in range(4):
            bins[i].append([])

    for i in range(size(CONCENTRATIONS)):
        for k in range(4):
            bins[i][k] = numpy.linspace(0, maxs[i][k]*1.1, 20)
            # bins[i][k] = numpy.linspace(mins[i][k]*0.9, maxs[i][k]*1.1, 20)
    print bins

elif Option == 2:
    for k in range(4):
        bins.append([])

    for k in range(4):
        maxs = numpy.matrix(maxs)
        print mins
        mins = numpy.matrix(mins)
        print "this is max: "+str(numpy.amax(maxs[:,k])*1.1)
        print maxs[:,k]
        bins[k] = numpy.linspace(numpy.amin(mins[:,k])*0.9, numpy.amax(maxs[:,k])*1.1, 20)
        # bins[i][k] = numpy.linspace(mins[i][k]*0.9, maxs[i][k]*1.1, 20)
    print bins


for i in range(size(datafiles)):
    execfile(datafiles[i])
    for j in range(size(CONCENTRATIONS)):
        grapher(Option)




show()
