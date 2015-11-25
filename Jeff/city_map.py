import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pickle
from mpl_toolkits.basemap import Basemap

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
print "Done."
print "Getting image corners..."
lower_left_lon,lower_left_lat = np.min(x),np.min(y)
upper_right_lon,upper_right_lat = np.max(x),np.max(y)
print "Done."
print "Creating figure and basemap..."
plt.figure(figsize=(16,12))
san_diego = Basemap(projection='cyl', llcrnrlat=lower_left_lat, \
                    urcrnrlat=upper_right_lat, llcrnrlon=lower_left_lon, \
                    urcrnrlon=upper_right_lon, resolution='f')
print "Done."
print "Drawing coastlines and continent..."
san_diego.drawcoastlines()
san_diego.fillcontinents(color='white', lake_color='blue', zorder=0)
print "Done."
print "Reading in county shapefile..."
san_diego.readshapefile('shape_data/sra/wgs84', 'sandiego')
print "Done."
# san_diego = Basemap(projection='cyl', llcrnrlat=32, urcrnrlat=34, llcrnrlon=-117.9, urcrnrlon=-116, resolution='i')
# san_diego.bluemarble()
print "Scattering points..."
converted_x,converted_y = san_diego(x, y)

# san_diego.scatter(converted_x, converted_y, marker='o', latlon=False, zorder=5, 
                    # c=color_sequence, edgecolor='face', alpha=0.5, s=magnitudes)
point_info = zip(x,y,color_sequence)
one_x = [lon for lon,_,color in point_info if color == '#FFFF00']
one_y = [lat for _,lat,color in point_info if color == '#FFFF00']
two_x = [lon for lon,_,color in point_info if color == '#FFA500']
two_y = [lat for _,lat,color in point_info if color == '#FFA500']
three_x = [lon for lon,_,color in point_info if color == '#8B0000']
three_y = [lat for _,lat,color in point_info if color == '#8B0000']
san_diego.scatter(two_x, two_y, marker='o', latlon=False, zorder=1, 
                    c='#FFA500', edgecolor='face', alpha=0.1, s=3)
san_diego.scatter(one_x, one_y, marker='o', latlon=False, zorder=3, 
                    c='#FFFF00', edgecolor='face', alpha=0.15, s=3)
san_diego.scatter(three_x, three_y, marker='o', latlon=False, zorder=5, 
                    c='#8B0000', edgecolor='face', alpha=0.05, s=3)

print len(one_x), len(two_x), len(three_x)
print "Done."
plt.title('Severity of crimes')
red = mpatches.Patch(color='#8B0000', label='Very severe')
orange = mpatches.Patch(color='#FFA500', label='Severe')
yellow = mpatches.Patch(color='#FFFF00', label='Moderate')
plt.legend(handles=[red, orange, yellow], title='Legend', ncol=1, loc=1)
# san_diego.plot(converted_x, converted_y, 'ro', alpha=0.01, markersize=3, markeredgecolor='red')
plt.show()
