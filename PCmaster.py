"""

Nathaniel Bloomfield

14/12/14

This code takes in the input and parses it to be analysed by any of the other modules.


Todo: fitting, and then

multi wavelength stuff... shouldn't be too hard.

For plotting multiple files - get them to merge the data together, and add an index before each well specification to say the plate number.

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


#code grabbed from online..... probably don't need this... Must be a better way to do this - with matplotlib

# import win32gui

# def window_switch():
#     toplist = []
#     winlist = []
#     def enum_callback(hwnd, results):
#         winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

#     win32gui.EnumWindows(enum_callback, toplist)
#     firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]
#     # just grab the first window that matches
#     firefox = firefox[0]
#     # use the window handle to set focus
#     return firefox


#functions and stuff

options = {'A' : 0,
                'B' : 12,
                'C' : 24,
                'D' : 36,
                'E' : 48,
                'F' : 60,
                'G' : 72,
                'H' : 84,
}

def RepresentsNotInt(s):
    try:
        int(s)
        return False
    except ValueError:
        return True

def choose_lambda():
    loop = False
    while loop == False:
        print 'What wavelength would you like to fit these curves at?'
        print "Available wavelengths: " + str(WAVELENGTHS)
        userinput = raw_input('Select the number wavelength you wish i.e. 1-'+str(size(WAVELENGTHS))+': ')
        if userinput.isdigit() == True and 0 < int(userinput) < size(WAVELENGTHS)+1:
            use_wavelength = int(userinput) -1
            break
        else:
            print "Invalid input, try again."
            continue
    return use_wavelength

def choose_fittedFile():
    print 'Would you like to also plot the fitted equations?'
    userinput = raw_input("Enter the filepath to fitted equations, or leave blank: ")
    return userinput

def equation(a,b,c,d):
    value = a*(1-numpy.exp(-b*TIME))**c +d
    return value

def lettertonum(a):

    for idx, val in enumerate(a):
        first = val[0]
        second = val[1]
        if RepresentsNotInt(first):
            first = options[val[0]]
            number = int(val[1:]) - 1
            new_val = first + number
        else:
            first = int(first)
            second = options[val[1]]
            number = int(val[2:]) - 1
            new_val = first*96 + second + number
        #print new_val
        a[idx] = new_val
    return a

def setup(ttot, t1, ti, CONC_WELLS, CONCENTRATIONS):

    TIME = []
    for i in range(ttot):
        TIME.append(t1+ i*ti)
    TIME = numpy.transpose(numpy.array(TIME))
    #print TIME
    #print TIME.shape

    CONC_WELLS_L = deepcopy(CONC_WELLS)
    #print id(CONC_WELLS_L)
    #print id(CONC_WELLS)

    CONC_WELLS_NEW = []
    for idx, val in enumerate(CONCENTRATIONS):
        CONC_WELLS_NEW.append([])
    return TIME, CONC_WELLS_L, CONC_WELLS_NEW


#actual coding

parser = argparse.ArgumentParser()
parser.add_argument('OPTION', type=str, nargs=1, choices=['examine','mean','fit'],
    help='State what action you wish to complete. Options are examine, mean, or fit.')
parser.add_argument('CONFIG', type=str, nargs=1, help='File path to the config file.')
parser.add_argument('CSV', type=str, nargs=1, help='File path to the CSV file.')
#should add support for multiple csv files later


parsed = parser.parse_args()   #parses sys.argv by default

#loading config file
execfile(parsed.CONFIG[0])

TIME, CONC_WELLS_L, CONC_WELLS_NEW = setup(ttot, t1, ti, CONC_WELLS, CONCENTRATIONS)

for idx, val in enumerate(CONC_WELLS):
    fiddling = CONC_WELLS[idx]
    fiddling = lettertonum(fiddling)
    CONC_WELLS[idx] = fiddling

data = genfromtxt(parsed.CSV[0], delimiter=',')

option = parsed.OPTION[0]

if option == "examine":
    execfile("PCexamine.py")
elif option == "mean":
    execfile("PCmean.py")
elif option == "fit":
    execfile("PCfit.py")
