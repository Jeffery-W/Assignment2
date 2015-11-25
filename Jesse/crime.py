import gzip
import numpy as np
from sklearn import svm
from sklearn.linear_model import Ridge
import numpy
from collections import defaultdict
import random
from random import randint
#{"gctype", "community", "month", "date", "is_night", "council", 
#"year", "id", "city", "asr_zone", "lon", "comm_pop", "type", "week",
#"gcquality", "address", "lat", "coun_pop", "day", "desc", "hour",
#"segment_id", "time", "lampdist", "nbrhood", "dow": "5"}
types = ["DRUGS/ALCOHOL VIOLATIONS", "THEFT/LARCENY", \
    "VEHICLE BREAK-IN/THEFT", "MOTOR VEHICLE THEFT", "BURGLARY", "VANDALISM", \
    "ASSAULT", "DUI", "FRAUD", "ROBBERY", "SEX CRIMES", "WEAPONS", "ARSON", \
    "HOMICIDE"]

total = []
with open('incidents-100k.json', 'r') as f:
    for line in f:
        total.append(eval(line))

training = total[:50000]
test = total[50000:]
print "Parsed Input File"

X_d = [[\
    float(entry['lat']), \
    float(entry['lon']), \
    #0 if (int(entry['dow']) == 0 or int(entry['dow']) == 6) else 1,\
    int(entry['asr_zone'])] \
    for entry in training if entry['is_night'] == "0" and float(entry['lat']) != 0.0]
y_d = [int(types.index(entry['type'])) for entry in training if entry['is_night'] == "0" and float(entry['lat']) != 0.0]

X_n = [[\
    float(entry['lat']), \
    float(entry['lon']), \
    int(entry['asr_zone'])]
    for entry in training if entry['is_night'] == "1" and float(entry['lat']) != 0.0]
y_n = [types.index(entry['type']) for entry in training if entry['is_night'] == "1" and float(entry['lat']) != 0.0]

print "Built Training and Test set"

clf_d = svm.SVC() #set C=100
clf_d.decision_function_shape='ovr'
clf_d.fit(X_d, y_d)

clf_n = svm.SVC()
clf_n.decision_function_shape='ovr'
clf_n.fit(X_n, y_n)

print "Created the model"

points = np.array([[float(entry['lat']), float(entry['lon']), int(entry['asr_zone']), \
                    int(entry['is_night']), types.index(entry['type'])] for \
            entry in test])
# [lat, lon, asr, night]
days = points[(points[:,-2] != 0)][:,0:-2]
days_actual = points[(points[:,-1] != 0)][:,-1]
nights = points[(points[:,-2] == 0)][:,0:-2]
nights_actual = points[(points[:,-1] == 0)][:,-1]

day_predicts = clf_d.predict(days)
night_predicts = clf_d.predict(nights)

predicts = np.concatenate((day_predicts,night_predicts))
actuals = np.concatenate((days_actual,nights_actual))
hamming = ((predicts^(actuals.astype(np.int64))).astype(np.float64)/len(types)).sum()/len(predicts)
print "Hamming loss: ", 1 - hamming
# diffsTest = []
# for i in range(0, len(test)):
#     print i
#     entry = test[i]
#     predict_test_y = 0
#     if entry['is_night'] == "0":
#         predict_test_y = clf_d.predict([\
#             float(entry['lat']), \
#             float(entry['lon']), \
#             #0 if (int(entry['dow']) == 0 or int(entry['dow']) == 6) else 1,\
#             int(entry['asr_zone']) \
#             ])
#     else:
#         predict_test_y = clf_n.predict([\
#             float(entry['lat']), \
#             float(entry['lon']), \
#             int(entry['asr_zone'])
#             ])

#     if (predict_test_y == types.index(entry['type'])):
#         diffsTest.append(1)
#     else:
#         diffsTest.append(0)

# print "Accuracy: ", sum(diffsTest)/float(len(diffsTest))
