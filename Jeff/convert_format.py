import csv
import pickle
fields = map(eval, open("fields").read().split(','))
print "Enter file to convert: ", 
f = open(raw_input())
print "Constructing dictionaries..."
reader = csv.DictReader(f, fields)
sample = list(reader)[1:]
print "Done."
for line in sample:
    for key in line:
        try:
            line[key] = eval(line[key])
        except:
            pass
f.close()
print "Enter pickle file name to write: ",
f = open(raw_input(), 'w')
pickle.dump(sample, f, 2)
f.close()
