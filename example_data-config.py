
print "config file loaded"


#First timestep, in seconds.

t1 = 20

#Every next timestep, in seconds. Timestep interval

ti = 180

#number of timesteps

ttot = 520

#Experimental conditions. This string will be used for plotting final graph

CONDITIONS = "37 Degrees, shaking"

#Concentrations. Use as many as you like.

CONC_UNIT = "uM"

CONCENTRATIONS = ['control', 0, 0.5, 5,50]
CONC_WELLS = list(CONCENTRATIONS)
CONC_WELLS[0] = ['A3', 'A10',  'B3', 'B10','C3', 'C10','D3', 'D10','E3', 'E10','F3', 'F10','G3', 'G10','H3', 'H10']
CONC_WELLS[1] = ['A1', 'A2',  'B1', 'B2','C1', 'C2','D1', 'D2','E1', 'E2','F1', 'F2','G1', 'G2','H1', 'H2']
CONC_WELLS[2] = ['A4', 'A5',  'B4', 'B5','C4', 'C5','D4', 'D5','E4', 'E5','F4', 'F5','G4', 'G5','H4', 'H5']
CONC_WELLS[3] = ['A8', 'A9',  'B8', 'B9','C8', 'C9','D8', 'D9','E8', 'E9','F8', 'F9','G8', 'G9','H8', 'H9']
CONC_WELLS[4] = ['A11', 'A12',  'B11', 'B12','C11', 'C12','D11', 'D12','E11', 'E12','F11', 'F12','G11', 'G12','H11', 'H12']

#Wavelengths

WAVELENGTHS = [440]


# end of editing section ----------------------------------------------

