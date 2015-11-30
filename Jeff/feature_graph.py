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

labels = [types[line['type']] for line in valid_crimes]

def plot_pkl(title, x):
    plt.clf()
    plt.plot(x, labels, 'co', alpha=0.5)
    plt.title(title)
    plt.show()

# # coords = [line for line in valid_crimes if line['lon'] != 0.0]
# asrs = [line['asr_zone'] for line in valid_crimes if line['asr_zone'] != '']
# # nbrs = [line for line in valid_crimes if line['nbrhood'] != 'NONE']
# # comms = [line for line in valid_crimes if line['community'] != 'NONE']
# pops = [line['comm_pop'] for line in valid_crimes if line['comm_pop'] != 0]
# coun_pops = [line['coun_pop'] for line in valid_crimes if line['coun_pop'] != 0]
# lampdists = [line['lampdist'] for line in valid_crimes if line['lampdist'] != '']

# plot_pkl("ASR Zones", asrs)
# # plot_pkl("Neighborhoods", asrs)
# # plot_pkl("Communities", )
# plot_pkl("Populations", pops)
# plot_pkl("Council populations", coun_pops)
# plot_pkl("Lamp distances", lampdists)
