import numpy as np
import pickle
from sklearn import svm
from sklearn.metrics import classification_report, hamming_loss

types = ["DRUGS/ALCOHOL VIOLATIONS", "THEFT/LARCENY", \
    "VEHICLE BREAK-IN/THEFT", "MOTOR VEHICLE THEFT", "BURGLARY", "VANDALISM", \
    "ASSAULT", "DUI", "FRAUD", "ROBBERY", "SEX CRIMES", "WEAPONS", "ARSON", \
    "HOMICIDE"]
# types = {crime:index for index,crime in enumerate(types)}
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
# total = []
# with open('incidents-100k.json', 'r') as f:
#     for line in f:
#         total.append(eval(line))
total = pickle.load(open("incidents_train.pkl"))
one_count,two_count,three_count = 0,0,0
training = []
i = len(total)-1
while len(training) < 30000:
    print i
    line = total[i]
    if line['type'] in three and three_count < 10000:
        three_count += 1
        training.append(line)
        total.pop(i)
    elif line['type'] in two and two_count < 10000:
        two_count += 1
        training.append(line)
        total.pop(i)
    elif line['type'] in one and one_count < 10000:
        one_count += 1
        training.append(line)
        total.pop(i)
    i -= 1

test = total
# training = total[:50000]
# test = total[50000:]
print "Parsed Input File"

X_d = [[entry['lat'], entry['lon'], entry['asr_zone']] \
    #0 if (int(entry['dow']) == 0 or int(entry['dow']) == 6) else 1,\
        for entry in training if entry['is_night'] == 0 and entry['lat'] != 0.0]
y_d = [types[entry['type']] for entry in training if entry['is_night'] == 0 and entry['lat'] != 0.0]

X_n = [[entry['lat'], entry['lon'], entry['asr_zone']] \
        for entry in training if entry['is_night'] == 1 and entry['lat'] != 0.0]
y_n = [types[entry['type']] for entry in training if entry['is_night'] == 1 and entry['lat'] != 0.0]

print "Built Training and Test set"

clf_d = svm.SVC() #set C=100
clf_d.decision_function_shape='ovr'
clf_d.fit(X_d, y_d)

clf_n = svm.SVC()
clf_n.decision_function_shape='ovr'
clf_n.fit(X_n, y_n)

print "Created the model"

points = np.array([[entry['lat'], entry['lon'], entry['asr_zone'], entry['is_night'],
                types[entry['type']]] for entry in test])
# points = np.array([[float(entry['lat']), float(entry['lon']), int(entry['asr_zone']), \
#                     int(entry['is_night']), types.index(entry['type'])] for \
#             entry in test])
# [lat, lon, asr, night]
days = points[(points[:,-2] != 0)][:,0:-2]
days_actual = points[(points[:,-1] != 0)][:,-1]
nights = points[(points[:,-2] == 0)][:,0:-2]
nights_actual = points[(points[:,-1] == 0)][:,-1]

day_predicts = clf_d.predict(days)
night_predicts = clf_d.predict(nights)

predicts = np.concatenate((day_predicts,night_predicts))
actuals = np.concatenate((days_actual,nights_actual))
# hamming = ((predicts^(actuals.astype(np.int64))).astype(np.float64)/len(types)).sum()/len(predicts)
hamming = ((predicts^(actuals.astype(np.int64))).astype(np.float64)/3).sum()/len(predicts)
# print "Hamming loss: ", hamming
actuals = actuals.astype(np.int64)
print classification_report(actuals, predicts)

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
