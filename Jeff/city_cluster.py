import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.cluster import KMeans

print "Reading data and extracting points..."
full_train = pickle.load(open("incidents_full_train.pkl"))
x = [line['lon'] for line in full_train if line['lon'] != 0.0]
y = [line['lat'] for line in full_train if line['lat'] != 0.0]
assert len(x) == len(y)
print "Done."
print "Calculating severity colors..."
three = ['ASSAULT', 'SEX CRIMES', 'HOMICIDE']
two = ['THEFT/LARCENY', 'VEHICLE BREAK-IN/THEFT', 'MOTOR VEHICLE THEFT', \
            'BURGLARY', 'VANDALISM', 'FRAUD', 'ROBBERY', 'ARSON']
one = ['DRUGS/ALCOHOL VIOLATIONS', 'DUI', 'WEAPONS']
colors = {}
for severity in three:
    colors[severity] = '#8B0000'
for severity in two:
    colors[severity] = '#FFA500'
for severity in one:
    colors[severity] = '#FFFF00'
color_sequence = [colors[line['type']] for line in full_train if line['lon'] != 0.0]
magnitudes = [3 if color == '#FFA500' else (5 if color == '#8B0000' else 2) for color in color_sequence]
assert len(x) == len(y) == len(color_sequence) == len(magnitudes)

clf = KMeans(n_clusters=10, n_jobs=4, 
