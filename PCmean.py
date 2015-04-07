"""

Nathaniel Bloomfield

14/12/14

This code takes input and after taking mean and SD, plots the data.

includes plotting each concentration series together, and also each concentration
at different wavelengths.

"""

MEAN = list(CONCENTRATIONS)
STD = list(CONCENTRATIONS)

TIME = TIME[:]/3600


#multiconcentration

for i in range(size(WAVELENGTHS)):
    fig = plt.figure()
    for idx, val in enumerate(CONC_WELLS):

        fiddling = CONC_WELLS[idx]
        MEAN[idx] = numpy.mean(data[ttot*i:ttot*(i+1),fiddling], axis=1)
        STD[idx] = numpy.std(data[ttot*i:ttot*(i+1),fiddling], axis=1)
        #STD_now = numpy.tile(STD[idx], (2,1))

        ax1 = fig.add_subplot(111)
        #print data[:,fiddling[idx2]].shape
        #ax1.plot(TIME,MEAN[idx])

        ax1.errorbar(TIME,MEAN[idx],yerr=STD[idx], errorevery=10, label=''+str(CONCENTRATIONS[idx])+CONC_UNIT+'')
        plt.draw()
        plt.pause(0.01)

    ax1.set_title('Multiconcentrations at '+str(WAVELENGTHS[i])+'nm: '+ CONDITIONS)
    plt.xlabel('Time (Hours)')
    plt.ylabel('Absorbance')
    plt.legend(loc='upper right')


#multiwavelength

for idx, val in enumerate(CONC_WELLS):

    fig = plt.figure()
    for i in range(size(WAVELENGTHS)):
        fiddling = CONC_WELLS[idx]
        MEAN[idx] = numpy.mean(data[ttot*i:ttot*(i+1),fiddling], axis=1)
        STD[idx] = numpy.std(data[ttot*i:ttot*(i+1),fiddling], axis=1)
        #STD_now = numpy.tile(STD[idx], (2,1))

        ax1 = fig.add_subplot(111)
        #print data[:,fiddling[idx2]].shape
        #ax1.plot(TIME,MEAN[idx])

        ax1.errorbar(TIME,MEAN[idx],yerr=STD[idx], errorevery=10, label=''+str(WAVELENGTHS[i])+'nm')
    ax1.set_title('Multiwavelength of '+str(CONCENTRATIONS[idx])+CONC_UNIT+' curves at '+ CONDITIONS)
    plt.xlabel('Time (Hours)')
    plt.ylabel('Absorbance')
    plt.legend(loc='upper right')
    plt.draw()
    plt.pause(0.01)



show()

