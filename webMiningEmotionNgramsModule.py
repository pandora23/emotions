
from nltk.corpus import wordnet as wn
#from nltk.corpus import wordnet_ic
from nltk.corpus import stopwords, words
from itertools import product
from nltk import FreqDist
#import pickle
import nltk
import json
import urllib2
import urllib
import re
import csv
#import Queue
from nltk import FreqDist
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
from scipy.stats.stats import pearsonr
#for web queries
import searchEngine
import sys

csv.field_size_limit(sys.maxsize)


emotions = list()


#get web results for each phrase,  use method
def getData(distance, numHits, strings):


    print(strings)
    results = []
    
    for string in strings:
    #web search here
        resultSet = searchEngine.getSearchResultsBing(string, numHits)

    for r in resultSet:
        results.append(r)
    
    #print(resultSet)
    
    #just building a frequency table for the web results as a whole
    allData = []

    #numTitles = len(results)
    keywords = nltk.word_tokenize(strings[0])
    stopwords = nltk.corpus.stopwords.words('english')
    words = nltk.corpus.words.words('en')
    
    
    for result in results[:]:
        
        #print(result)
        if(result != "http://ppaquarium.com/"
           and result != "http://www.john-tom.com/RCtank/RCTank.html"):
            
            
            accepted = False
            try:
                #go to site and get webpage

                try:
                    #url = "https://" + result
                    url = result
                    print(url)
                    page = urllib2.urlopen(url).read()
                    #print(page)

                except:
                    #url = "http://" + result
                    page = urllib2.urlopen(url).read()
                    #print(page)
                    

                accepted = True

                #clean up page
                page = nltk.clean_html(page)

                page = re.sub('[;:.,`\"\'-]','',page)

                page = nltk.word_tokenize(page)

                #print(page)
                
            except:

                #print("DIDNTWORK")
                pass

    

            if accepted == True and 'feel' in page:
                ngram = ['feel']    
                pageTokens = []
                
                for word in ngram:
                    #grab all indexes
                    indexList = []
                    i = -1
                    try:
                        while True:
                            i = page.index(word, i+1)
                            indexList.append(i)
                    except:
                        pass

                    #DISTANCE TO TARGET
                    distanceFromTarget = distance
                    
                    try:
                        for index in indexList:
                            if index < distanceFromTarget:
                                pageTokens = pageTokens + page[:(index+distanceFromTarget)]
                            if (index + distanceFromTarget) >= len(page):
                                pageTokens = pageTokens + page[(index-distanceFromTarget):]
                            else:
                                pageTokens = pageTokens + page[(index-distanceFromTarget):(index+distanceFromTarget)]
                    except:
                        pass

                print("PageTokens")
                #print(pageTokens)
                docTokens = []
                try:
                    
                    if pageTokens != []:
                        print('notempt')
                        docTokens  = [token.lower() for token in pageTokens if token.lower() not in stopwords
                                      and token.lower() in words and len(token.lower()) > 1 and token.lower() not in ngram
                                      and token.lower() not in ['happy', 'sad']]
                except:
                    pass

                #print('dt')
                #print(docTokens)
                if docTokens != []:
                    #print(docTokens)
                    emotions.append(' '.join(docTokens))

    #print("ALLDATA:")
    #print(allData)
    #print("ALL")
    #print(allData)
    return 1



d = 5
n = 35000
getData(d,n,['+happy +feel -lyrics'])
hcount = len(emotions)
print(hcount)

getData(d,n,['+sad +feel -lyrics'])

def genMatrixCSV(ngwidth, booleanize):
    freqVectors = []
    ngWidth=ngwidth

    bigramVectorizer = CountVectorizer(stop_words = 'english', ngram_range=(1,ngWidth), token_pattern=r'\b\w+\b',min_df=1, max_features = 200000);

    transformed = bigramVectorizer.fit_transform(emotions)
    tags = bigramVectorizer.get_feature_names()

    labels = []
    for entry in tags:
        entry = entry.replace(' ', '_')
        labels.append(entry)

    tags = labels 

    numDocs = min(hcount, len(emotions)-hcount)
    print(numDocs)
    print(hcount)
    print(len(emotions)-hcount)

    #output to CSV
    with open('emotionData25NG' + str(ngwidth) + 'BAG' + str(booleanize) + '.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        tags.append('emotion1')
        
        writer.writerow(tags)
        for vec in transformed[:numDocs]:
            
            v = vec.toarray()[0].tolist()
            if booleanize:
                for i in range(len(v)):
                    if v[i] > 0:
                        v[i] = 1
            v.append('HAPPY')
            writer.writerow(v)
        for vec in transformed[hcount+1:hcount+1+numDocs]:
            
            v = vec.toarray()[0].tolist()
            if booleanize:
                for i in range(len(v)):
                    if v[i] > 0:
                        v[i] = 1
            v.append('SAD')
            writer.writerow(v)

#convert to csv files
genMatrixCSV(1, True)
genMatrixCSV(2, True)
genMatrixCSV(1, False)
genMatrixCSV(2, False)

    

