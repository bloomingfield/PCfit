"""
Written by:
Nathaniel Bloomfield

14/12/14

This code fits a curve to the data it, outputing the data reduction as a .py file.

"""


def string_strip(a):
    string = a
    if string.endswith('.py'):
        string = string[:-3]
    elif string.endswith('.csv'):
        string = string[:-4]

    while ('/' in string) == True:
        string = string[string.find('/')+1:]
        print string

    return string



def next_step(a, b, c, d, a_low,a_high,b_low, b_high,c_low, c_high,d_low, d_high):
    global NAD, NBD, NCD, NDD

    a_int = a_high - a_low

    a_low = a - a_int/NAD
    a_high = a + a_int/NAD

    b_int = b_high - b_low

    b_low = b - b_int/NBD
    b_high = b + b_int/NBD

    c_int = c_high - c_low

    c_low = c - c_int/NCD
    c_high = c + c_int/NCD

    d_int = d_high - d_low

    d_low = d - d_int/NDD
    d_high = d + d_int/NDD

    return a_low, a_high, b_low, b_high, c_low, c_high, d_low, d_high


def fitting_func(a_low,a_high,b_low, b_high,c_low, c_high,d_low, d_high):
    global NAD, NBD, NCD, NDD, ttot, data, fiddling, idx2
    a=numpy.linspace(a_low, a_high, NAD)
    b=numpy.linspace(b_low, b_high, NBD)
    c=numpy.linspace(c_low, c_high, NCD)
    d=numpy.linspace(d_low, d_high, NDD)

    SSQ_guess = 10**(10)
    condition = [1,1,1,1]
    m=0
    for u in range(size(a)):
        a_use = a[u]
        for j in range(size(b)):
            b_use = b[j]
            for k in range(size(c)):
                c_use = c[k]
                for l in range(size(d)):
                    #print m
                    m+=1
                    d_use = d[l]
                    value = equation(a_use, b_use, c_use, d_use)
                    SSQ_trial=numpy.sum((data[ttot*use_wavelength:ttot*(use_wavelength+1),fiddling[idx2]]-(value))**2)
                    if SSQ_trial < SSQ_guess:
                       SSQ_guess = SSQ_trial
                       condition = [u,j,k,l]
    return a[condition[0]], b[condition[1]], c[condition[2]], d[condition[3]]



use_wavelength = choose_lambda()

NAD = 10
NBD = 30
NCD = 30
NDD = 1

#Not working with buffer
CONCENTRATIONS = (CONCENTRATIONS[1:])
CONC_WELLS = (CONC_WELLS[1:])
CONC_WELLS_L = CONC_WELLS_L[1:]


CONC_WELLS_CONST = []
for idx, val in enumerate(CONCENTRATIONS):
        CONC_WELLS_CONST.append([])
#print CONC_WELLS_CONST
TIME_old = deepcopy(TIME)
data_old = deepcopy(data)
ttot_old2 = ttot

plotting = True
fig = plt.figure()


for idx, val in enumerate(CONC_WELLS):

    fiddling = CONC_WELLS[idx]

    for idx2, val2 in enumerate(fiddling):

        #Smoothing stuff
        # i = 0
        # ttot = ttot_old2
        # TIME = TIME_old
        # while i < ttot-1:

        #     if numpy.abs(data[i,fiddling[idx2]] - data[i+1,fiddling[idx2]]) > 0.015:
        #         ttot_old = ttot
        #         ttot= ttot -1
        #         data[:ttot,fiddling[idx2]] = numpy.delete(data[:ttot_old,fiddling[idx2]], i+1)
        #         TIME = numpy.delete(TIME, i+1)
        #         continue
        #     else:
        #         i += 1
        #         continue

        # d = numpy.amin(data[(ttot*use_wavelength):ttot*(use_wavelength +1),fiddling[idx2]])
        # print d
        # a = numpy.amax(data[(ttot*use_wavelength):ttot*(use_wavelength +1),fiddling[idx2]] - d)
        # print a


        # d = numpy.sum(data[(ttot*use_wavelength):(ttot*use_wavelength +6),fiddling[idx2]])/6
        # # print d
        # a = numpy.sum(data[(ttot*(use_wavelength+1)-5):(ttot*(use_wavelength+1)),fiddling[idx2]] - d)/6
        # print a
        d = numpy.amin(data[(ttot*use_wavelength):(ttot*(use_wavelength+1)),fiddling[idx2]] )
        d_low = d*1
        d_high = d*1
        a = numpy.amax(data[(ttot*use_wavelength):(ttot*(use_wavelength+1)),fiddling[idx2]] - d)
        a_low = a*1
        a_high = a*1.1

        b_low = 1e-06
        b_high = 2e-04
        c_low = 1
        c_high = 3

        a, b, c, d = fitting_func(a_low,a_high,b_low, b_high,c_low, c_high,d_low, d_high)

        #could tidy up this bit.
        a_low, a_high, b_low, b_high, c_low, c_high, d_low, d_high = next_step(a, b, c, d, a_low,a_high,b_low, b_high,c_low, c_high,d_low, d_high)

        a, b, c, d = fitting_func(a_low,a_high,b_low, b_high,c_low, c_high,d_low, d_high)

        CONST = [a, b, c, d]
        CONC_WELLS_CONST[idx].append(CONST)

        value = equation(a, b, c, d)
        #print value
        print str(a)+ ', ' + str(b)+ ', ' + str(c) + ', ' + str(d)

        #plot each one
        if (plotting):
            print plt.get_fignums()
            if size(plt.get_fignums()) > 20:
                plt.close('all')
            plt.clf()

            ax1 = fig.add_subplot(111)
            ax1.plot(TIME,data[:ttot,fiddling[idx2]], 'ro', mfc='None' , label="Data")
            # ax1.plot(TIME_old,data_old[:ttot_old2,fiddling[idx2]], 'rx' , label="Data")
            ax1.plot(TIME,value, 'r-', label="Fitting curve")
            ax1.set_title('Fitting empirical function to well '+CONC_WELLS_L[idx][idx2]+' at '+
                str(CONCENTRATIONS[idx])+CONC_UNIT+', '+ CONDITIONS+', '+str(WAVELENGTHS[use_wavelength])+'nm')
            plt.xlabel('Time (Hours)')
            plt.ylabel('Absorbance')
            plt.legend(loc='lower right')
            plt.draw()
            plt.pause(0.01)



#print CONC_WELLS_CONST

config = string_strip(parsed.CONFIG[0])
csv = string_strip(parsed.CSV[0])

filename =  csv+'-'+config+'-datareduction.py'

with open(filename, 'wb') as writefile:

    for idx, val in enumerate(CONC_WELLS_CONST):

        CONC_WELLS_CONST[idx] = numpy.array(CONC_WELLS_CONST[idx])

    writefile.write('# This data reduction was completed using the python software suite written by Nathaniel Bloomfield. \n')
    write = str(parsed.CSV[0])
    writefile.write('csvFile = "' + write+'"\n')
    write = str(parsed.CONFIG[0])
    writefile.write('configFile ="' + write+'"\n')
    writefile.write('from numpy import array \n')
    write = str(WAVELENGTHS[use_wavelength])
    writefile.write('use_wavelength =  '+ write +'\n')
    write = str(CONDITIONS)
    writefile.write('CONDITIONS = \'' + write +'\'\n')
    write = str(CONCENTRATIONS)
    writefile.write('CONCENTRATIONS = ' + write+'\n')
    write = str(CONC_UNIT)
    writefile.write('CONC_UNIT =\'' + write +'\'\n')
    write = str(CONC_WELLS_CONST)
    writefile.write('CONC_WELLS_CONST = ' + write+'\n')


show()
