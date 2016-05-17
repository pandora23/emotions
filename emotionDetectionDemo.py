from sklearn.ensemble import RandomForestClassifier

import numpy as np
import csvInOutEmotion

data = csvInOutEmotion.getData('emotionDataTab26f.csv')

rfc = RandomForestClassifier(n_estimators=100)

xval = []
yval = []

labels = data[0]

x = data[1:]
for f in data[1:]:
    xval.append(f[:-1])
    yval.append(f[len(f)-1])
    

rfc.fit(xval, yval)

zipped = zip(rfc.feature_importances_, labels)

def getKey(item):
    return item[0]

sortZipped = sorted(zipped, key=getKey)


##km = KMeans(n_clusters=8, init='k-means++', max_iter=300, n_init=1, verbose=True)
##
##km.fit(data[1:])
##
##labels = data[0]
##
##clusterNum = 1
##
##index = 0
##
##for center in km.cluster_centers_:
##    index = 0
##    print('Cluster number ' + str(clusterNum))
##    clusterNum = clusterNum + 1
##    nextString = ''
##    for val in center:
##        if val > 0.2:
##            nextString = nextString + ', ' + labels[index]
##        index = index + 1
##    print('Significant keywords: ')
##    print(nextString)
##

