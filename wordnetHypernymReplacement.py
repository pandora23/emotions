#given data frame X indicating occurence of words w1..wn for vectors v1..vn add hypernyms of non ambiguous words
#example  apple->fruit,  see if there is improvement


from nltk.corpus import wordnet as wn


def addHypernyms(vecs, labels):
    #not implemented yet
    xVecs = vecs
    
    results = []
    
    newLabels = labels[:]
    labelCount = len(labels)
    numNewCounts = 0
    
    for vec in xVecs:
        newVec = vec
        for i in range(numNewCounts):
            newVec.append(0)
            
        hypernyms = []
        print("next")
        counter = 0
        
        for count in vec[:labelCount]:
            word = labels[counter]
            counter = counter + 1
            if count > 0:
                print(word)
                synsets = wn.synsets(word)
                print(len(synsets))
                #increase count if already in labels
                #otherwise add to hypernym vector
                if len(synsets) >= 1:
                    print("One synset")
                    print(word)
                    hypernym = synsets[0].hypernyms()[0].name[:-5]
                    if hypernym in newLabels:
                        hInd = newLabels.index(hypernym)
                        newVec[hInd] = newVec[hInd] + 1
                    else:
                        newLabels.append(hypernym)
                        #extend the count vector for all vectors
                        
                        newVec.append(1)
                        numNewCounts = numNewCounts + 1
                    #finish after this cryptic web search
        results.append(newVec)
    return results, newLabels
    
def replaceKeywordsWithHypernyms():
    print('not implemented')

#test

testL = ['apple', 'fruit', 'tank', 'printer', 'eat', 'pineapple', 'dishsoap', 'carrot']
testV =[[1,1,1,1,1,1,1,1],[0,1,0,1,0,1,0,1],[0,0,0,0,1,1,1,1],[1,1,1,1,0,0,0,0]]

newV, newL = addHypernyms(testV, testL)
