
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

    numTitles = len(results)
    keywords = nltk.word_tokenize(strings[0])
    stopwords = nltk.corpus.stopwords.words('english')
    words = nltk.corpus.words.words()
    
    
    for result in results:
        
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


            if accepted == True:
                
                pageTokens = []
                
                for word in strings:
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
                                #print("Adding")
                                pageTokens.append(page[:(index+distanceFromTarget)])
                            if (index + distanceFromTarget) >= len(page):
                                #print("Adding")
                                pageTokens.append(page[(index-distanceFromTarget):])
                            else:
                                #print("Adding")
                                pageTokens.append(page[(index-distanceFromTarget):(index+distanceFromTarget)])
                    except:
                        pass

                print("PageTokens")
                print(pageTokens)
                docTokens = []
                try:
                    #print("PT")
                    #print(pageTokens)
                    
                    #pageTokens = [word.lower() for word in pageTokens if word in words and word.lower() not in keywords
                     #         and word not in stopwords]
                    if pageTokens != []:
                        for set1 in pageTokens:
                            for token in set1:
                                #print(type(token))
                                if isinstance(token, str):
                                    if token.lower() not in stopwords and token.lower() not in strings and token.lower() in words:
                                        #print('tk:')
                                        #print(token.lower())
                                        docTokens.append(token.lower())
                except:
                    pass

                if docTokens != []:
                #wordSets.append(set(docTokens))
                    emotions.append(' '.join(docTokens))

    #print("ALLDATA:")
    #print(allData)
    print("ALL")
    print(allData)
    return 1



d = 5
n = 50
getData(d,n,['happy'])
hcount = len(emotions)
print(hcount)

getData(d,n,['sad'])


#frequencies
freqVectors = []
ngWidth=1

bigramVectorizer = CountVectorizer(stop_words = 'english', ngram_range=(1,ngWidth), token_pattern=r'\b\w+\b',min_df=1, max_features = 500);

transformed = bigramVectorizer.fit_transform(emotions)

tags = bigramVectorizer.get_feature_names()

#tfidf next after finishing this





#output to CSV
with open('emotionDataTab26.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    tags.append('emotion1')
    
    writer.writerow(tags)
    for vec in transformed[:hcount]:
        v = vec.toarray()[0].tolist()
        v.append('HAPPY')
        writer.writerow(v)
    for vec in transformed[hcount+1:]:
        v = vec.toarray()[0].tolist()
        v.append('SAD')
        writer.writerow(v)


        
        


