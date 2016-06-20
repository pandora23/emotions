#print off high frequency words given data frame containing vectors v1...vn
import numpy as np
import csvInOutEmotion


def printSortedCounts(num, xVecs, labels):
    #sum the colums, sort by total count, print
    sums = np.zeros(len(xVecs[0]))
    for v in xVecs:
        for i in xrange(len(v)):
            sums[i] = sums[i] + int(v[i])
    counts = zip(sums,labels)
    sortedCounts = sorted(counts, key=lambda x: x[0], reverse=True)
    print(sortedCounts[:num])


#do so for happy and then for sad

#test

vs= [[1,2,3],[0,1,0],[10,0,5]]
ls= ['apple','bark','tree']
printSortedCounts(2,vs,ls)

#usage on dataset from web mining
data = csvInOutEmotion.getData('emotionData25NG2BAGFalse.csv')
xval = []
labels1 = data[0][:-1]
for f in data[1:]:
        xval.append(f[:-1])
mid = int(len(xval)/2)

#happy
topN =  30
print(str(topN) + " highest count n-grams co-occuring with 'feel' given a happy context: ")
printSortedCounts(topN, xval[:mid], labels1)
print(str(topN) + " highest count n-grams co-occuring with 'feel' given a sad context: ")
printSortedCounts(topN, xval[mid+1:], labels1)

