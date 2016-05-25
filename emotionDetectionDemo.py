from sklearn.ensemble import RandomForestClassifier

import numpy as np
import csvInOutEmotion

data = csvInOutEmotion.getData('emotionDataTab26f2rr.csv')

rfc = RandomForestClassifier(n_estimators=2, max_depth=1)

xval = []
yval = []

labels = data[0][:-1]

x = data[1:]
for f in data[1:]:
    xval.append(f[:-1])
    yval.append(f[len(f)-1])
    

rfc.fit(xval, yval)

zipped = zip(rfc.feature_importances_, labels)

def getKey(item):
    return item[0]

sortZipped = sorted(zipped, key=getKey)


#4 will refactor later, example diary entries
d1 = ['clap']
d2 = ['low']
d3 = ['effective']
d4 = ['happiness']


diaries = list()
diaries.append(d1)
diaries.append(d2)
diaries.append(d3)
diaries.append(d4)


#build vectors for prediction

diaryVectors = list()

diaryVectors.append([])
diaryVectors.append([])
diaryVectors.append([])
diaryVectors.append([])



for i in labels:
    for k in range(4):
        if i in diaries[k]:
            print(i)
            diaryVectors[k].append(1)
        else:
            diaryVectors[k].append(0)


for v in diaryVectors:
    print(rfc.predict(v))




##        
##    if i in d1:
##        v1.append(1)
##    else:
##        v1.append(0)
##    
##    if i in d2:
##        v2.append(1)
##    else:
##        v1.append(0)
##
##






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

