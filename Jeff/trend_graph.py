import pickle
import numpy as np
import matplotlib.pyplot as plt

types = {}
three = ['ASSAULT', 'SEX CRIMES', 'HOMICIDE']
two = ['THEFT/LARCENY', 'VEHICLE BREAK-IN/THEFT', 'MOTOR VEHICLE THEFT', \
            'BURGLARY', 'VANDALISM', 'FRAUD', 'ROBBERY', 'ARSON']
one = ['DRUGS/ALCOHOL VIOLATIONS', 'DUI', 'WEAPONS']
for crime in three:
    types[crime] = 2
for crime in two:
    types[crime] = 1
for crime in one:
    types[crime] = 0

valid_crimes = pickle.load(open("valid_crimes.pkl"))