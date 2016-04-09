"""
Written by:
Nathaniel Bloomfield

14/12/14

This plots the datareduction files.

"""
# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib
matplotlib.use('tkagg')
from pylab import *
import numpy
import argparse
import re
# matplotlib.use('qt4agg')
# matplotlib.use('tkagg') - this produces freezing when drawing LOBF's on windows
matplotlib.rc('font', family='serif')


def choose_option():
    loop = False

    print 'Would you like to compare conditions or concentrations?'
    print "Press 1 to compare conditions, and 2 to compare concentrations "

    while loop == False:
        userinput = raw_input('Select the number you wish: ')
        if userinput.isdigit() == True and 0 < int(userinput) < 3:
            Option = int(userinput)
            break
        else:
            print "Invalid input, try again."
            continue

    print 'What kind of graph would you like to produce?'
    print "Press 1 to create a histogram, and 2 to create a scatter plot"

    while loop == False:
        userinput = raw_input('Select the number you wish: ')
        if userinput.isdigit() == True and 0 < int(userinput) < 3:
            Graphtype = int(userinput)
            break
        else:
            print "Invalid input, try again."
            continue

    return Option, Graphtype


def grapher_histogram (Option):
    fiddling = dataHolder[j]
    for k in range(4):
        weight = np.ones_like(fiddling[:,k])/len(fiddling[:,k])
        mu = numpy.mean(fiddling[:,k], axis=0)
        sigma = numpy.std(fiddling[:,k], axis=0)

        if Option == 1:
            plt.figure(str(k)+str(j))
            plt.hist(fiddling[:,k], bins[j][k], alpha=0.5,  label=conditionList[j] , weights = weight)
            plt.suptitle('Fitted '+ parameter[k]+' at wavelength '+str(use_wavelength)+'nm and concentration '+ str(concentrationList[j])+CONC_UNIT)
            plt.annotate(conditionList[j], xy=(mu, 0.0),  xycoords='data',
                xytext=(0, 10*i+50), textcoords='offset points',
                arrowprops=dict( shrink=0.05),
                horizontalalignment='center', verticalalignment='center',
                )
        elif Option == 2:
            plt.figure(conditionList[j]+str(k))
            plt.hist(fiddling[:,k], bins[k], alpha=0.5,  label=str(concentrationList[j]) , weights = weight)
            plt.suptitle('Fitted '+ parameter[k]+' at wavelength '+str(use_wavelength)+'nm')
            plt.annotate(str(concentrationList[j]), xy=(mu, 0.0),  xycoords='data',
                xytext=(0, 10*i+50), textcoords='offset points',
                arrowprops=dict( shrink=0.05),
                horizontalalignment='center', verticalalignment='center',
                )

        plt.xlabel('Value of parameter '+ parameter[k])
        plt.ylabel('Frequency')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.draw()
        plt.pause(0.1)



def grapher_scatter (Option):

    Avar = dataHolder[j][:, 0]
    Bvar = dataHolder[j][:, 1]
    Cvar = dataHolder[j][:, 2]

    for k in range(6):

        if 0 <= k <= 3:
            fiddling = dataHolder[j][:, k]
        elif k == 4:
            fiddling = numpy.divide(numpy.log(Cvar), Bvar)
            fiddling = numpy.ma.masked_less(fiddling, 0)
            # print fiddling
        elif k == 5:
            fiddling = numpy.multiply(Avar, numpy.multiply(Bvar,
                    numpy.power(numpy.divide((Cvar - 1), Cvar), (Cvar - 1))))
            fiddling = numpy.ma.masked_invalid(fiddling)
            # print fiddling


        mu = numpy.ma.mean(fiddling, axis=0)
        sigma = numpy.ma.std(fiddling, axis=0)

        if Option == 1:

            CONDnumber = int(re.search(r'\d+', conditionList[j]).group())

            plt.figure(str(k)+str(concentrationList[j]))
            # print "this is my bannana "+str(CONDnumber)

            plotData = numpy.vstack(
                (CONDnumber*numpy.ones_like(fiddling), fiddling))
            plt.scatter(plotData[0, :], plotData[1, :], alpha=0.5, c='r')

            characteristicNumber = CONDnumber

            plt.scatter(CONDnumber, mu, marker='x', s=100,  facecolors='none', edgecolors='k')
            plt.scatter(CONDnumber, mu + sigma, marker='^', s=100,facecolors='none', edgecolors='k')
            plt.scatter(CONDnumber, mu - sigma, marker='v', s=100, facecolors='none', edgecolors='k')

            # plt.suptitle('Fitted '+ parameter[k]+' at wavelength '+str(use_wavelength)+'nm and concentration '+ str(concentrationList[j])+CONC_UNIT)

            plt.xlabel('Temperature (degrees Celsius)')

            LOBFindex = dataToFit[0].index(str(concentrationList[j]))

        elif Option == 2:

            plt.figure(str(k)+str(conditionList[j]))

            plotData = numpy.vstack(
                (concentrationList[j]*numpy.ones_like(fiddling), fiddling))
            # print plotData
            characteristicNumber = concentrationList[j]

            plt.scatter(plotData[0, :], plotData[1, :], alpha=0.5, c='r')

            plt.scatter(concentrationList[j], mu, marker='x', s=100,  facecolors='none', edgecolors='k')
            plt.scatter(concentrationList[j], mu + sigma, marker='^', s=100,facecolors='none', edgecolors='k')
            plt.scatter(concentrationList[j], mu - sigma, marker='v', s=100, facecolors='none', edgecolors='k')

            plt.xlabel("Concentration ("+CONC_UNIT+")")

            LOBFindex = dataToFit[0].index(str(conditionList[j]))
            # print LOBFindex
            # print dataToFit[1][k][LOBFindex][0]
            # print dataToFit[1][k][LOBFindex][0].shape
            # print concentrationList[j]

        # print plotData.shape
        dataToFit[1][k][LOBFindex][0] = numpy.concatenate(
            (dataToFit[1][k][LOBFindex][0], plotData), axis=1)

        print "{} : {} : \\num{{{:.2e}}} $\pm$ \\num{{{:.2e}}}".format(characteristicNumber, parameter[k], float(mu), float(sigma))
        # str(characteristicNumber)+" : "+str(parameter[k])+" : "+str(mu) +" $\pm$ " + str(sigma)
        plt.ylabel('Value of parameter '+ parameter[k])
        plt.grid(True)
        plt.draw()
        plt.pause(0.1)

def grapher_LOBF():
    # print  dataToFit
    for j in range(len(dataToFit[0])):
        for k in range(6):
            plt.figure(str(k)+str(dataToFit[0][j]))
            fiddling = dataToFit[1][k][j][0]
            fiddling = numpy.ma.masked_less(fiddling, 0)
            fiddling = numpy.ma.masked_invalid(fiddling)
            fiddling = numpy.ma.mask_rowcols(fiddling, axis=1)
            # print fiddling
            idx = np.isfinite(fiddling[0, :]) & np.isfinite(fiddling[1, :])
            polynomial = numpy.ma.polyfit(fiddling[0, idx], fiddling[1, idx], 1)
            polynomial2 = numpy.ma.polyfit(fiddling[0, idx], fiddling[1, idx], 2)
            # print 'this is polynomial: '+str(polynomial)
            xDraw = numpy.linspace(numpy.ma.min(fiddling[0, :]),
                                   numpy.ma.max(fiddling[0, :]), num=100)
            # print 'this is xdraw: '+str(xDraw)
            polynomialDraw = numpy.polyval(polynomial, xDraw)
            polynomialDraw2 = numpy.polyval(polynomial2, xDraw)
            # print 'this is polydraw: '+str(polynomialDraw)
            plt.plot(xDraw, polynomialDraw, 'b-')
            plt.plot(xDraw, polynomialDraw2, 'g-')

            axes = plt.gca()
            axes.set_ylim(0,
                numpy.amax(fiddling[1, :])*1.1)
            if k == 3:
                axes = plt.gca()
                axes.set_ylim(numpy.amin(fiddling[1, :])*0.99,
                    numpy.amax(fiddling[1, :])*1.01)
            elif k == 4:
                axes = plt.gca()
                axes.set_ylim(0,
                    numpy.amax(fiddling[1, :])*1.1)
                # axes.set_xlim(10, 110)
            elif k == 5:
                axes = plt.gca()
                axes.set_ylim(0,
                    numpy.amax(fiddling[1, :])*1.1)

            plt.draw()
            plt.pause(0.1)

def minMax (Option):
    global datafiles

# this needs redoing. It currently only picks one datafile to initialise first array, and assumes
# all datafiles have the same number of concentrations. I don't like this code - too messy.


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
                thisArray[i].append([1000000])
    print thisArray
    for i in range(size(datafiles)):
        with open(datafiles[i]) as f:
            carryData = {}
            code = compile(f.read(), datafiles[i], 'exec')
            exec(code, carryData)

        for j in range(size(carryData['CONCENTRATIONS'])):
            print 'j = '+str(j)
            middleMe = carryData['CONC_WELLS_CONST']
            fiddling = middleMe[j]
            for k in range(4):
                # print 'k = '+str(k)
                if Option == 'max':
                    tests = numpy.amax(fiddling[:,k])
                    if tests > thisArray[j][k]:
                        thisArray[j][k] = tests
                elif Option == 'min':
                    tests = numpy.amin(fiddling[:,k])
                    if tests < thisArray[j][k]:
                        thisArray[j][k] = tests
    return thisArray

parameter = {0 : 'A',
                1 : 'B',
                2 : 'C',
                3 : 'D',
                4 : r"$\frac{1}{B}\log(C)$ (lag time)",
                5 : r"$AB(\frac{C-1}{C})^{C-1}$ (maximal steepness)",
}

conditionList = [];
concentrationList = [];


# Start of program

parser = argparse.ArgumentParser()
parser.add_argument('DATA', type=str, nargs='*', help='File path to the reduced data file.')
#should add support for multiple csv files later

parsed = parser.parse_args()   #parses sys.argv by default

Option, Graphtype = choose_option()


#loading config file
datafiles = parsed.DATA

maxs = minMax('max')
mins = minMax('min')

print maxs
print mins

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
    # print bins

elif Option == 2:
    for k in range(4):
        bins.append([])

    for k in range(4):
        maxs = numpy.matrix(maxs)
        # print mins
        mins = numpy.matrix(mins)
        # print "this is max: "+str(numpy.amax(maxs[:,k])*1.1)
        # print maxs[:,k]
        bins[k] = numpy.linspace(numpy.amin(mins[:,k])*0.9, numpy.amax(maxs[:,k])*1.1, 20)
        # bins[i][k] = numpy.linspace(mins[i][k]*0.9, maxs[i][k]*1.1, 20)
    # print bins
    # print bins[k][0]
    # print bins[k][-1]

conditionList = [];
concentrationList = [];
dataHolder = [];
for i in range(size(datafiles)):
    execfile(datafiles[i])
    for j in range(size(CONCENTRATIONS)):
        sameConditionIndices = [i for i, x in enumerate(conditionList) if x == CONDITIONS]
        sameConcentrationIndices = [i for i, x in enumerate(concentrationList) if x == CONCENTRATIONS[j]]
        # print 'condition indices '+str(sameConditionIndices)
        # print 'concentration indices ' +str(sameConcentrationIndices)
        intersectionIs = [val for val in sameConditionIndices if val in sameConcentrationIndices]
        # print intersectionIs
        if intersectionIs == []:
            conditionList.append(CONDITIONS)
            concentrationList.append(CONCENTRATIONS[j])
            dataHolder.append(CONC_WELLS_CONST[j])
        elif size(intersectionIs) == 1:
            dataHolder[intersectionIs[0]] = numpy.concatenate((dataHolder[intersectionIs[0]], CONC_WELLS_CONST[j]), axis=0)
        else:
            print intersectionIs
# print conditionList
# print concentrationList
# print dataHolder

if Option == 1:
    FittingList = list(set(concentrationList))
elif Option == 2:
    FittingList = list(set(conditionList))


dataToFit = [FittingList, [[ [ np.array([[], []])] for i in range(len(FittingList))] for i in range(6)] ]


for j in range(size(conditionList)):
    if Graphtype == 1:
        grapher_histogram(Option)
    elif Graphtype == 2:
        # print FittingList
        # print len(FittingList)
        # print dataToFit
        grapher_scatter(Option)

if Graphtype == 2:
        grapher_LOBF()

plt.show()
