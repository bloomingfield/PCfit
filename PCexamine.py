
"""

Nathaniel Bloomfield

14/12/14

This code takes input and displays each graph in turn.

Should do this at highest wavelength - or let people choose.
Because highest wavelength would be easiest to tell if condensation was occuring and graph could be thrown out.

"""

use_wavelength = choose_lambda()
use_fittedFile = choose_fittedFile()

if use_fittedFile != '':
    with open(use_fittedFile) as f:
        carryData = {}
        code = compile(f.read(), use_fittedFile, 'exec')
        exec(code, carryData)
    middleMe = carryData['CONC_WELLS_CONST']
    CONC_WELLS_CONST_NEW = []
    for idx, val in enumerate(middleMe):
        CONC_WELLS_CONST_NEW.append([])


fig = plt.figure()

if use_fittedFile != '':
    indexIterate = middleMe
else:
    indexIterate = CONC_WELLS

for idx, val in enumerate(indexIterate):
    if use_fittedFile != '':
        fiddlingFitted = middleMe[idx]
        dataIdx = idx +1
        fiddling = CONC_WELLS[dataIdx]
    else:
        fiddling = CONC_WELLS[idx]
        dataIdx = idx

    for idx2, val2 in enumerate(fiddling):
        ax1 = fig.add_subplot(111)
        #print data[:,fiddling[idx2]].shape

        ax1.plot(TIME,data[ttot*use_wavelength:ttot*(use_wavelength+1),fiddling[idx2]], 'ro', mfc='None' )
        if use_fittedFile != '':
            fittedData = equation(fiddlingFitted[idx2,0],fiddlingFitted[idx2,1],fiddlingFitted[idx2,2],fiddlingFitted[idx2,3])
            ax1.plot(TIME,fittedData, 'r-' )
        ax1.set_title('Well: '+ CONC_WELLS_L[dataIdx][idx2] +', Concentration: '+ str(CONCENTRATIONS[dataIdx]))
        # thismanager = get_current_fig_manager()
        # thismanager.window.wm_geometry("+0+0")
        plt.draw()
        plt.pause(0.01)
        loop = False
        while loop == False:
            #print idx2
            userinput = raw_input('Is this graph okay? Press enter to accept, or n to reject: ')
            # firefox = window_switch()
            # win32gui.SetForegroundWindow(firefox[0])
            if userinput == '':
                if use_fittedFile != '':
                    CONC_WELLS_CONST_NEW[idx].append(fiddlingFitted[idx2, :])
                else:
                    CONC_WELLS_NEW[idx].append(CONC_WELLS_L[dataIdx][idx2])
                print "Graph accepted"
                break
            elif userinput == 'n':
                print "Graph rejected"
                break
            else:
                print "Invalid input, try again."
                continue
        plt.clf()


if use_fittedFile != '':
    with open(use_fittedFile, "a") as NEW_FITTED:

        for idx, val in enumerate(CONC_WELLS_CONST_NEW):

            CONC_WELLS_CONST_NEW[idx] = numpy.array(CONC_WELLS_CONST_NEW[idx])

        NEW_FITTED.write('CONC_WELLS_CONST = '+str(CONC_WELLS_CONST_NEW))

else:
    with open(parsed.CONFIG[0], "a") as NEW_CONFIG:
        for idx, val in enumerate(CONC_WELLS_NEW):
            array = '\', \''.join(CONC_WELLS_NEW[idx])
            NEW_CONFIG.write("CONC_WELLS["+str(idx)+"] = [\'" + array + "\'] \n")


