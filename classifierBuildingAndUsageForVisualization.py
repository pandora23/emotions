from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pydot

import numpy as np
import csvInOutEmotion

bestScore = 0
bestClassifier = None
labels = None

def buildClassifier(ngWid, booleanized, depth, sampleN):
    data = csvInOutEmotion.getData('emotionDataNG' + str(ngWid) + 'BAG' + str(booleanized) + '.csv')
    

    #random forest exploration
    #rfc = RandomForestClassifier(n_estimators=10, max_depth=2)

    #decisiontree sklearn
    classifier = tree.DecisionTreeClassifier(max_depth=depth, min_samples_leaf=sampleN)

    xval = []
    yval = []

    global labels;
    labels = data[0][:-1]

    x = data[1:]
    for f in data[1:]:
        xval.append(f[:-1])
        yval.append(f[len(f)-1])

    split = int(len(xval)*3/4/2)
    #print(split)
    
    mid = int(len(xval)/2)
    #print(mid)
    
    xtrain = xval[:split] + xval[mid:mid+split]
    ytrain = yval[:split] + yval[mid:mid+split]

    #print(len(xtrain))
    #print(len(ytrain))

    
    xtest = xval[split+1:mid] + xval[mid+split:]
    ytest = yval[split+1:mid] + yval[mid+split:]

    #print(ytest)

    #rfc.fit(xval, yval)

    #split for cross val
    classifier.fit(xtrain, ytrain)

            
    #score on testing data
    score= classifier.score(xtest, ytest)
    global bestScore
    global bestClassifier
    if score > bestScore:
        bestClassifier = classifier
        bestScore = score
        

    #ypredictions
    #ypredictionsTrain = classifier.predict(xtrain)
    #print(ypredictionsTrain)
    
    print("Classifier score on test for treeNG" + str(ngWid) + 'BAG' + str(booleanized) + 'depth' + str(depth) + 'leafMin' + str(sampleN)+":" + str(score))
    #rint(score)

    #feature importances according to random forest
    ##    zipped = zip(rfc.feature_importances_, labels)

    def getKey(item):
        return item[0]
    #sortZipped = sorted(zipped, key=getKey)

    #draw decision tree
    with open("tree1.dot","w") as f:
        f = tree.export_graphviz(classifier, out_file=f)

    dot_data = StringIO()
    tree.export_graphviz(classifier, out_file=dot_data, feature_names=labels)
    graph  = pydot.graph_from_dot_data(dot_data.getvalue())
    graph.write_pdf("2treeNG" + str(ngWid) + 'BAG' + str(booleanized) + 'depth' + str(depth) + 'leafMin' + str(sampleN))
    return classifier


#build classifiers with different parameters
classifiers = []
ngWidths = [1,2]
bools = [True, False]
depths = [100,110]
leafMins = [2,3]
for w in ngWidths:
    for b in bools:
        for d in depths:
            for m in leafMins:
                classifiers.append(buildClassifier(w,b,d,m))
            

#test with fake diary entry co-occuring words



#4 will refactor later, example diary entries
d1 = ['bad']
d2 = ['good']
d3 = ['awful']
d4 = ['great']
d5 = ['crying']
d6 = ['dancing']
d7 = ['sadness']
d8 = ['happyness']
##d9 = ['like_crying']
##d10 = ['nice']
##d11 = ['sick']
##d12 = ['up']
##d13 = ['down']


diaries = list()
diaries.append(d1)
diaries.append(d2)
diaries.append(d3)
diaries.append(d4)
diaries.append(d5)
diaries.append(d6)
diaries.append(d7)
diaries.append(d8)
##diaries.append(d9)
##diaries.append(d10)
##diaries.append(d11)
##diaries.append(d12)
##diaries.append(d13)

#build vectors for prediction

diaryVectors = list()

for i in range(len(diaries)):
    diaryVectors.append([])

#turn diaries to word occurence vector
for i in labels:
    for k in range(len(diaries)):
        if i in diaries[k]:
            print(i)
            diaryVectors[k].append(1)
        else:
            diaryVectors[k].append(0)

#predict diaries



x = []
y = []
z = []

time = 0
for v in diaryVectors:
    prediction = bestClassifier.predict(v)
    print(bestClassifier.predict(v))
    if prediction == 'HAPPY':
        print('yes')
        x.append(1)
        y.append(0)
        z.append(time)
    else:
        y.append(1)
        x.append(0)
        z.append(time)
        
    time = time+1


fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot(x,y,z)
plt.show()
        



#zipped2 = zip(classifier.feature_importances_, labels)
#s2 = sorted(zipped2, key=getKey)



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

