import numpy as np
import pickle
import random
from collections import defaultdict

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

print "Reading data..."
label_counts = defaultdict(int)
full_train = pickle.load(open("incidents_full_train.pkl"))
for line in full_train:
    label_counts[types[line['type']]] += 1
print "Done."
print label_counts

label_counts = defaultdict(int)
days = [line for line in full_train if line['is_night'] == 0]
for line in days:
    label_counts[types[line['type']]] += 1
print label_counts
nights = [line for line in full_train if line['is_night'] == 1]
label_counts = defaultdict(int)
for line in nights:
    label_counts[types[line['type']]] += 1
print label_counts

def check_valid(crime):
    return crime['asr_zone'] != '' and crime['lat'] != 0.0

# goal is to build balanced day, night for train,test
# so day -> 45k, night -> 45k
# so severities = 15k each
def build_dataset(dataset):
    one_count,two_count,three_count = 0,0,0
    train = []
    old_length = len(dataset)
    i = len(dataset)-1
    while len(train) < 24000:
        # print i
        line = dataset[i]
        if line['type'] in three and three_count < 8000 and check_valid(line):
            three_count += 1
            train.append(line)
            dataset.pop(i)
        elif line['type'] in two and two_count < 8000 and check_valid(line):
            two_count += 1
            train.append(line)
            dataset.pop(i)
        elif line['type'] in one and one_count < 8000 and check_valid(line):
            one_count += 1
            train.append(line)
            dataset.pop(i)
        i -= 1
    print old_length, len(dataset)
    return train

print "Building train set from day data..."
train_days = build_dataset(days)
print "Done."
print "Building train set from night data..."
train_nights = build_dataset(nights)
print "Done."

print "Building test set from day data..."
test_days = build_dataset(days)
print "Done."
print "Building test set from night data..."
test_nights = build_dataset(nights)
print "Done."

train = train_days + train_nights
test = test_days + test_nights

print "Shuffling..."
random.seed(0)
random.shuffle(train)
random.shuffle(test)
print "Done."

print "Pickling data..."
f = open("incidents_balanced_train.pkl", 'w')
pickle.dump(train, f, 2)
f.close()

f = open("incidents_balanced_test.pkl", 'w')
pickle.dump(test, f, 2)
f.close()
print "Done."

