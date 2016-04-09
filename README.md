# PCfit

These scripts require python, numpy and matplotlib. To use these scripts, first arrange the progress curve data as in the example config and example csv file. To inspect each progress curve use the command

python PCmaster.py examine CONFIG CSV

This will display graphs of each of the raw progress curves, and give you the option of rejecting them. It will append the new data set to the config file. This is useful for visualising and removing erroneous replicates. It also has the option to visualize each individual fit as well (after using the fit module - explained later on). If you wish to plot some sample curves at different conditions, use command

python PCmaster.py examinesome CONFIG CSV

To plot the mean and standard deviation of the raw data, use the command

python PCmaster.py mean CONFIG CSV

To fit to the empirical function A(D-Exp[-Bt])**C using a least squares method, use the command below

python PCmaster.py fit CONFIG CSV

You may need to tweak the variables to get a decent fit. It will output a new file called CSV-CONFIG-datareduction.py, which records all the fitted constants for the raw data. There is a second module which deals with the output file described above. The command for calling it is

python PCplotfit.py reduced_data_1 reduced_data_2 reduced_data_3 ...

This module can take multiple reduced data files, and tries to amalgamate them together. It can either compare conditions, or concentrations, and has the option to plot the data as a scatter plot, or as a histogram.
