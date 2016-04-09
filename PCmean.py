"""
Written by:
Nathaniel Bloomfield

14/12/14

This code takes takes the mean and standard deviation of the data, and displays it as a graph.

"""

MEAN = list(CONCENTRATIONS)
STD = list(CONCENTRATIONS)
INHIBITION = list(CONCENTRATIONS)
TIME = TIME[:]/3600
inhibitionAssay = True

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
        if (inhibitionAssay):
            if (idx > 0):
                INHIBITION[idx] =  (1 - MEAN[idx][-1]/MEAN[1][-1])*100

    ax1.set_title('Multiconcentrations at '+str(WAVELENGTHS[i])+'nm: '+ CONDITIONS)
    plt.xlabel('Time (Hours)')
    plt.ylabel('Absorbance')
    plt.legend(loc='best')

    if (inhibitionAssay):

        polynomial = numpy.ma.polyfit(CONCENTRATIONS[1:], INHIBITION[1:], 3)
        xDraw = numpy.linspace(0,
                               CONCENTRATIONS[-1], num=100)
        polynomialDraw = numpy.polyval(polynomial, xDraw)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot( CONCENTRATIONS[1:], INHIBITION[1:], 'ro', mfc='None' )
        ax.plot(xDraw, polynomialDraw, 'b-')
        ax.set_title('IC50 value at '+ CONDITIONS)
        ax.set_xlim(-1, CONCENTRATIONS[-1] + 1)
        ax.set_ylim(-1,  101)
        plt.grid(True)
        plt.yticks(np.linspace(0, 100, 11))
        plt.xlabel('Concentration of Inhibitor ('+CONC_UNIT+')')
        plt.ylabel('% Inhibition')
        # print INHIBITION[1:]
        # print CONCENTRATIONS[1:]


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
    plt.legend(loc='best')
    plt.draw()
    plt.pause(0.01)



show()

