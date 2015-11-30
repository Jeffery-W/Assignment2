import pickle
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.metrics import hamming_loss
from pprint import pprint

print "Reading data..."
X = pickle.load(open("train_features.pkl"))
y = pickle.load(open("train_labels.pkl"))
points = pickle.load(open("test_features.pkl"))
actuals = pickle.load(open("test_labels.pkl"))
print "Done."

clfs = []
clfs.append((RandomForestClassifier(n_estimators=300, n_jobs=4), "random forest"))
clfs.append((DecisionTreeClassifier(), "decision tree"))
clfs.append((KNeighborsClassifier(n_neighbors=200, n_jobs=4, algorithm='kd_tree', weights='distance'), "K-neighbors"))
clfs.append((LogisticRegressionCV(Cs=[0.001, 0.01, 0.1, 1.0, 1.5], solver='lbfgs', refit=True, multi_class='multinomial'), "logistic regression with cross-validation"))
clfs.append((NearestCentroid(metric='euclidean'), "nearest centroid"))
clfs.append((ExtraTreesClassifier(n_estimators=300, n_jobs=4, max_features=7), "extremely randomized trees"))
losses = []
for clf,name in clfs:
    print "Fitting using " + name + "..."
    clf.fit(X, y)
    print "Done."
    print "Predicting..."
    predicts = clf.predict(points)
    print "Done."
    losses.append((1 - hamming_loss(actuals, predicts), name))

pprint(losses)
losses = sorted(losses, reverse=True)
print "Best: ", losses[0]
