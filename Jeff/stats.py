import numpy as np
import pickle
import matplotlib.pyplot as plt
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
full_train = pickle.load(open("incidents_full_train.pkl"))
print "Done."
size = float(len(full_train))/100
print "Full set size: ", len(full_train)
fields = full_train[0].keys()
print "Data fields: ", ", ".join(fields)
print "Statistics on full set of crimes: ", 
days = [line for line in full_train if line['is_night'] == 0]
nights = [line for line in full_train if line['is_night'] == 1]
print "Number of day crimes: ", len(days)
print "Percentage: ", len(days)/size
print "Number of night crimes: ", len(nights)
print "Percentage: ", len(nights)/size
crime_counts = defaultdict(int)
for line in full_train:
    crime_counts[line['type']] += 1
print "Number of crimes per offense category: "
total_crimes = sum(crime_counts.values())
for crime in crime_counts:
    print crime + ": ", crime_counts[crime]
print "Total crimes: ", total_crimes

total_crimes = float(total_crimes)/100
severity_counts = defaultdict(int)
for line in full_train:
    severity_counts[types[line['type']]] += 1
print "Number of crimes per crime type: "
print "Personal crime: ", severity_counts[2]
print "Percentage: ", severity_counts[2]/total_crimes
print "Property crime: ", severity_counts[1]
print "Percentage: ", severity_counts[1]/total_crimes
print "Statutory crime: ", severity_counts[0]
print "Percentage: ", severity_counts[0]/total_crimes

invalid_coords = [line for line in full_train if line['lon'] == 0.0]
print "Number of crimes with invalid coordinates: ", len(invalid_coords)
print "Percentage: ", len(invalid_coords)/size
invalid_asrs = [line for line in full_train if line['asr_zone'] == '']
print "Number of crimes with missing ASR zone: ", len(invalid_asrs)
print "Percentage: ", len(invalid_asrs)/size
invalid_nbr = [line for line in full_train if line['nbrhood'] == 'NONE']
print "Number of crimes with missing neighborhood: ", len(invalid_nbr)
print "Percentage: ", len(invalid_nbr)/size
invalid_comm = [line for line in full_train if line['community'] == 'NONE']
print "Number of crimes with missing community: ", len(invalid_comm)
print "Percentage: ", len(invalid_comm)/size
invalid_pop = [line for line in full_train if line['comm_pop'] == 0]
print "Number of crimes with invalid populations: ", len(invalid_pop)
print "Percentage: ", len(invalid_pop)/size
invalid_coun_pop = [line for line in full_train if line['coun_pop'] == 0]
print "Number of crimes with invalid council populations: ", len(invalid_coun_pop)
print "Percentage: ", len(invalid_coun_pop)/size
invalid_dists = [line for line in full_train if line['lampdist'] == '']
print "Number of crimes with invalid lamp distances: ", len(invalid_dists)
print "Percentage: ", len(invalid_dists)/size

def check_valid(crime):
    return crime['lon'] != 0.0 and crime['asr_zone'] != '' and crime['nbrhood'] != 'NONE' and crime['community'] != 'NONE' and crime['comm_pop'] != 0 and crime['lampdist'] != '' and crime['coun_pop'] != 0

valid_crimes = [line for line in full_train if check_valid(line)]
size = float(len(valid_crimes))/100
print "Number of crimes with clean data: ", len(valid_crimes)
print "Percentage: ", len(valid_crimes)/size

print "Statistics on valid crimes: "
day_numbers = [line['day'] for line in valid_crimes]
print "Day range: ", np.min(day_numbers), '-', np.max(day_numbers)
weeks = [line['week'] for line in valid_crimes]
print "Week range: ", np.min(weeks), '-', np.max(weeks)
months = [line['month'] for line in valid_crimes]
print "Month range: ", np.min(months), '-', np.max(months)
years = [line['year'] for line in valid_crimes]
print "Year range: ", np.min(years), '-', np.max(years)
lons = [line['lon'] for line in valid_crimes]
print "Longitude range: ", np.min(lons), '-', np.max(lons)
lats = [line['lat'] for line in valid_crimes]
print "Latitude range: ", np.min(lats), '-', np.max(lats)
lampdists = [line['lampdist'] for line in valid_crimes]
print "Lamp distance range: ", np.min(lampdists), '-', np.max(lampdists)
days = [line for line in valid_crimes if line['is_night'] == 0]
nights = [line for line in valid_crimes if line['is_night'] == 1]
print "Number of day crimes: ", len(days)
print "Percentage: ", len(days)/size
print "Number of night crimes: ", len(nights)
print "Percentage: ", len(nights)/size
crime_counts = defaultdict(int)
for line in valid_crimes:
    crime_counts[line['type']] += 1
print "Number of crimes per offense category: "
total_crimes = sum(crime_counts.values())
for crime in crime_counts:
    print crime + ": ", crime_counts[crime]
print "Total crimes: ", total_crimes


total_crimes = float(total_crimes)/100
severity_counts = defaultdict(int)
for line in valid_crimes:
    severity_counts[types[line['type']]] += 1
print "Number of crimes per crime type: "
print "Personal crime: ", severity_counts[2]
print "Percentage: ", severity_counts[2]/total_crimes
print "Property crime: ", severity_counts[1]
print "Percentage: ", severity_counts[1]/total_crimes
print "Statutory crime: ", severity_counts[0]
print "Percentage: ", severity_counts[0]/total_crimes

day_severities = defaultdict(int)
night_severities = defaultdict(int)
for line in valid_crimes:
    if line['is_night'] == 0:
        day_severities[types[line['type']]] += 1
    else:
        night_severities[types[line['type']]] += 1
print "Number of day/night crimes per crime type: "
print "Personal crime, day: ", day_severities[2]
print "Personal crime, night: ", night_severities[2]
print "Property crime, day: ", day_severities[1]
print "Property crime, night: ", night_severities[1]
print "Statutory crime, day: ", day_severities[0]
print "Statutory crime, night: ", night_severities[0]


dows = defaultdict(int)
for line in valid_crimes:
    dows[line['dow']] += 1
dow_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
print "Number of crimes per day of week: "
for day in range(7):
    print dow_names[day] + ": ", dows[day]

dow_severities = []
for day in range(7):
    dow_severity = defaultdict(int)
    dow_crimes = [line for line in valid_crimes if line['dow'] == day]
    for crime in dow_crimes:
        dow_severity[types[crime['type']]] += 1
    dow_severities.append([dow_severity[0], dow_severity[1], dow_severity[2]])
print "Number of crimes per day by type:"
for day in range(7):
    print dow_names[day] + ": "
    print "Personal crime: ", dow_severities[day][2]
    print "Property crime: ", dow_severities[day][1]
    print "Statutory crime: ", dow_severities[day][0]

