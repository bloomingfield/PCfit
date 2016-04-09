
"""
Written by:
Nathaniel Bloomfield

14/12/14

This code allows several individual curves to be displayed at once.

"""

def choose_some():
    loop = False
    while loop == False:
        print 'What wells would you like to plot the data together for?'
        print 'Cannot select buffer wells and a best fit curve at the same time.'
        print "Seperate each one by a space. e.g. A11 A12 B13"
        userinput = raw_input('Please type in the cells you wish: ')
        break
    return userinput


use_wavelength = choose_lambda()
use_fittedFile = choose_fittedFile()

if use_fittedFile != '':
    with open(use_fittedFile) as f:
        carryData = {}
        code = compile(f.read(), use_fittedFile, 'exec')
        exec(code, carryData)
    middleMe = carryData['CONC_WELLS_CONST']


loop = False
while loop == False:
    chosenSome = choose_some().split()
    print chosenSome
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # ax1.set_title('Multi-concentration sample fit')
    chosenSome_L = deepcopy(chosenSome)
    chosenSome = lettertonum(chosenSome)
    print chosenSome

    for idx, val in enumerate(chosenSome):

        for idx2, val2 in enumerate(CONC_WELLS):
            try:
                inList = CONC_WELLS[idx2].index(val)
            except:
                print "Not in concentration "+str(idx2)
            else:
                inElement = inList
                inConcentration = idx2
                inConcentrationName = CONCENTRATIONS[idx2]
                print inConcentration
                print inConcentrationName


        fiddlingFitted = middleMe[inConcentration-1]
        #print data[:,fiddling[idx2]].shape

        ax1.plot(TIME,data[ttot*use_wavelength:ttot*(use_wavelength+1),val], 'ro', mfc='None' )
        if use_fittedFile != '':
            fittedData = equation(fiddlingFitted[inElement,0],fiddlingFitted[inElement,1],
                fiddlingFitted[inElement,2],fiddlingFitted[inElement,3])
            ax1.plot(TIME,fittedData, label=unicode(inConcentrationName)+unicode(CONC_UNIT) )
        plt.legend(loc='upper left')
        # thismanager = get_current_fig_manager()
        # thismanager.window.wm_geometry("+0+0")
        plt.draw()
        plt.pause(0.01)

    userinput = raw_input('Is this graph okay? Press enter to redraw: ')

    if userinput == '':
        plt.clf()
        continue



plt.show()
