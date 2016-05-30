from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.externals.six import StringIO

import pydot

import numpy as np
import csvInOutEmotion

data = csvInOutEmotion.getData('emotionDataTab26f2rrrrZBIGRAM.csv')

#random forest exploration
rfc = RandomForestClassifier(n_estimators=10, max_depth=2)

#decisiontree sklearn
classifier = tree.DecisionTreeClassifier(max_depth=1000, min_samples_leaf=3)

xval = []
yval = []




labels = data[0][:-1]

x = data[1:]
for f in data[1:]:
    xval.append(f[:-1])
    yval.append(f[len(f)-1])

split = int(len(xval)*2/3)
xtrain = xval[:split]
ytrain = yval[:split]
xtest = xval[split+1:]
ytest = yval[split+1:]


rfc.fit(xval, yval)

#split for cross val
classifier.fit(xtrain, ytrain)

#score on testing data
score= classifier.score(xtest, ytest)
print("Classifier score on test: ")
print(score)

#feature importances according to random forest
zipped = zip(rfc.feature_importances_, labels)

def getKey(item):
    return item[0]
sortZipped = sorted(zipped, key=getKey)



#4 will refactor later, example diary entries
d1 = ['bad']
d2 = ['good']
d3 = ['awful']
d4 = ['great']
d5 = ['crying']
d6 = ['dancing']
d7 = ['sadness']
d8 = ['happyness']



diaries = list()
diaries.append(d1)
diaries.append(d2)
diaries.append(d3)
diaries.append(d4)
diaries.append(d5)
diaries.append(d6)
diaries.append(d7)
diaries.append(d8)

#build vectors for prediction

diaryVectors = list()

diaryVectors.append([])
diaryVectors.append([])
diaryVectors.append([])
diaryVectors.append([])
diaryVectors.append([])
diaryVectors.append([])
diaryVectors.append([])
diaryVectors.append([])



for i in labels:
    for k in range(8):
        if i in diaries[k]:
            print(i)
            diaryVectors[k].append(1)
        else:
            diaryVectors[k].append(0)


for v in diaryVectors:
    print(classifier.predict(v))


with open("tree1.dot","w") as f:
    f = tree.export_graphviz(classifier, out_file=f)

dot_data = StringIO()
tree.export_graphviz(classifier, out_file=dot_data, feature_names=labels)
graph  = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("tre1.pdf")

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


zipped2 = zip(classifier.feature_importances_, labels)

s2 = sorted(zipped2, key=getKey)



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

