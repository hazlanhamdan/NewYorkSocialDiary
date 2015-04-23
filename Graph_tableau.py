
#####################################################################################################################################################################
###    Author: Shatrunjai Singh
###
###    Title: The New york social circle
###
###    Date: 04/05/2015
###
###    Purpose: To probe the new york social diary (website) to find which people appear more in pictures
###    and which people tend to occur together
###
###    Description: [New York Social Diary](http://www.newyorksocialdiary.com/) provides a fascinating lens onto New York's socially well-to-do.
###    The data forms a natural social graph for New York's social elite.  Take a look at this page of a recent run-of-the-mill holiday party:
###    http://www.newyorksocialdiary.com/party-pictures/2014/holiday-dinners-and-doers`
###    Besides the brand-name celebrities, we notice the photos have carefully annotated captions labeling those that appear in the photos.  We can think of this as implicitly implying a social graph: there is a connection between two individuals if they appear in a picture together.
###    The first step is to fetch the data.  This comes in two phases.The first step is to crawl the data.  We want photos from parties before December 1st, 2014.  From
###    http://www.newyorksocialdiary.com/party-pictures to see a list of (party) pages.  For each party's page, we grab all the captions.
###    After we have a list of all captions, we save the data on disk so that you can quickly retrieve it.  Now comes the parsing part.
###    
###    For the analysis, we think of the problem in terms of a [network](http://en.wikipedia.org/wiki/Computer_network) or a [graph](http://en.wikipedia.org/wiki/Graph_%28mathematics%29).  Any time a pair of people appear in a photo together, that is considered a link.  What we have described is more appropriately called an (undirected) [multigraph](http://en.wikipedia.org/wiki/Multigraph) with no self-loops but this has an obvious analog in terms of an undirected [weighted graph](http://en.wikipedia.org/wiki/Graph_%28mathematics%29#Weighted_graph).  In this problem, we will analyze the social graph of the new york social elite.
###    For this problem, we use python's `networkx` library.
###
###    Questions asked:    1.) The simplest question we might want to ask is 'who is the most popular'?  The easiest way to answer this question is to look at how many connections everyone has.
###
###                        2.) A similar way to determine popularity is to look at their [pagerank](http://en.wikipedia.org/wiki/PageRank).
###                            Pagerank is used for web ranking and was originally
###                            [patented](http://patft.uspto.gov/netacgi/nph-Parser?patentnumber=6285999) by Google and is essentially the
###                            [stationary distribution](http://en.wikipedia.org/wiki/Markov_chain#Stationary_distribution_relation_to_eigenvectors_and_simplices)
###                            of a [markov chain](http://en.wikipedia.org/wiki/Markov_chain) implied by the social graph.
###                            Use 0.85 as the damping parameter so that there is a 15% chance of jumping to another vertex.
###
###                        3.) Another interesting question is who tends to co-occur with each other.  
###
###                                                                                                                                                                                                                                                                                                                                    
########################################################################################################################################################################


import os.path
import sys
import urllib2
import json
import re
import numpy as np
import urlparse
import requests
from nltk import *
from bs4 import BeautifulSoup
from nltk.tag import pos_tag
from multiprocessing import Pool
import networkx as nx
import itertools
workers = Pool(30)


#The code below crawls  www.newyorksocialdiary.com and stores the content into an object called pagesoup (of the class beautiful soup). The links
# to different pages are then extracted from this object and sent to another function, get_photo_caption(), which actually extracts the 
# photocaptions from these different picture pages.         

def get_photo_caption(photo_url): # function to get the photocaptions from these different pages
    try:        
        photo_page='http://www.newyorksocialdiary.com'+str(photo_url)
        print photo_page
        r=requests.get(photo_page)
        r.content
        photo_soup=BeautifulSoup(r.content)
        namestext=photo_soup.find_all("div",{"class":"photocaption"})
        for names in namestext:
            names=names.text
            print names   #the photocaptions are printed to the screen and saved as a text file, c:/data/Names2ANSI2.txt
           
            
    except Exception, f:
        y=f
        print "Hell broke loose in get_photo_caption function!"+str(y)
        
        
def get_pages(): # function to get all the links to different photopages
    try:          
                for page in range(1,25):   #number of pages to crawl, less than 25     
                    url="http://www.newyorksocialdiary.com/party-pictures?page="+str(page)                   
                    page_url=requests.get(url)                    
                    page_url.content
                    pagesoup=BeautifulSoup(page_url.content)
                    for link in pagesoup.find_all('a'):
                        actual_link_picture_page=str(link.get('href')) # extracts the actual link of the page from the whole <a> href: thingy
                        if (len(str(actual_link_picture_page))> 25) and (actual_link_picture_page[0]=="/") :
                           get_photo_caption(actual_link_picture_page)                      
                                             
               
            
    except Exception, e:
        z=e
        print "Shit went bad in get_page function!"+str(z)    
        
get_pages()


#Function langpro() uses the photocaptions saved in the file Names2ANSI.txt and uses the Natural Language Processing Library (NLTK) to 
#tokenize, chunk and identify person names (NNP tags). Finally list comprehensions are used to clean up the names generated (Removing '/NNP', etc.)

def langpro(item):
    try:
        tokenized=nltk.word_tokenize(item)
        tagged=nltk.pos_tag(tokenized)     
        chunkgram= r"""Chunk: {<NNP>+}""" 
        chunkparser=nltk.RegexpParser(chunkgram)
        chunked=chunkparser.parse(tagged)
        entities=re.findall(r'Chunk(.+)',str(chunked))
        #code to clean up data
        entities = [(w.replace('/NNP', '')) for w in entities]
        entities = [(w.replace(')', '')) for w in entities]
        entities = [(w.replace('(', '')) for w in entities]
        entities = [(w.replace('and', ',')) for w in entities]
        entities = [(w.replace(']', '')) for w in entities]
        entities = [(w.replace('/CC', '')) for w in entities]        
        print entities #the final names are printed to the screen and stored in a txt file named : names-after-re.txt
     
    except Exception, f:
        y=f
        print "Hell broke loose in get nltp area!"+str(y)

    
f=open('c:/data/Names2ANSI.txt', 'r') #open the picture tags previously saved in the last section
for line in iter (f):    
    langpro(line)
f.close()    


#Alternate to Natural Language Processing we can use regular expressions (RE library) to find 2 capitalized words in a row. However this 
# is less accurate than the Natural Language Processing (NLTK library). Also it recuqires us to manually remove a bunch of false positives we recieve

"""

def findword(item):
    try:
        
            if (len(str(item))<250):
                
                item=str(item)
                item= item.replace("von","Von")
                item= item.replace("van","Van")
                item= item.replace("de","De")
                sentense= str(re.findall(r'''([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)''',item))
                sentense = sentense.replace("Council ","")
                sentense = sentense.replace("Councilman ","")
                sentense = sentense.replace("Councilmember ","")
                sentense = sentense.replace("Councilwoman ","")
                sentense = sentense.replace("Congresswoman ","")
                sentense = sentense.replace("New York","")
                sentense = sentense.replace("Board","")
                sentense = sentense.replace("Member","")
                sentense = sentense.replace("Congressman ","")
                sentense = sentense.replace("Gala","")
                sentense = sentense.replace("History","")
                sentense = sentense.replace("Museum","")
                sentense = sentense.replace("American","")
                sentense = sentense.replace("Congressman ","")
                sentense = sentense.replace("Night ","")
                sentense = sentense.replace("Miss ","")
                sentense = sentense.replace("USA ","")         
                sentense = sentense.replace("Mayor ","")
                sentense = sentense.replace("Event Co","")
                sentense = sentense.replace("Count ","")
                sentense = sentense.replace("Countess ","")
                sentense = sentense.replace("Chairman ","")
                sentense = sentense.replace("Chairwoman ","")
                sentense = sentense.replace("President ","")
                sentense = sentense.replace("Meuseum ","")
                sentense = sentense.replace("Chairmen ","")
                sentense = sentense.replace("DJ ","")
                sentense = sentense.replace("MD ","")
                sentense = sentense.replace("Dance ","")
                sentense = sentense.replace("Director ","")
                sentense = sentense.replace("Dr. ","")
                sentense = sentense.replace("Sir ","")
                sentense = sentense.replace("The ","")
                sentense = sentense.replace("Society","")
                sentense = sentense.replace("Memorial Sloan","")                
                sentense = sentense.replace("Jr. ","")
                sentense = sentense.replace("CEO ","")
                sentense = sentense.replace("[", "")
                sentense = sentense.replace("]", "")
                sentense = sentense.replace("' ", "'")
                sentense = sentense.replace(" ' ", "'")
                sentense = sentense.replace(" '", "'")
                sentense = sentense.replace("'", "")
                sentense = sentense.replace("Executive Director","")
                sentense = sentense.replace("Presi","")
                sentense = sentense.replace("Co ","")
                sentense = sentense.replace("Steering Committee ","")
                sentense = sentense.replace("Vice Presi ","")
                
                return list(sentense.split(','))
           
            
    except Exception, f:
        y=f
        print "Hell broke loose in get nltp area!"+str(y)


#To open the crawled list of names from the website and feed it into the function findword which will find different names in the text.
list_of_words=[]    
f=open('c:/data/Names2ANSI2.txt', 'r') 
for line in iter (f):
    w=findword(line)
    list_of_words.append(w)
f.close()
list_of_words = [x for x in list_of_words if x != []]

"""


# open the list of names stored in 'names-after-re.txt' and create combinations of all the names present in a photograph together.
# for example a photo with 3 names creates 3 tuples with all possible non-repeated combinations. This would help us later when adding 
# nodes into the graph and maping relationships. We use the networkx library in python to create this graph.

data_combo=[]
data=[]
f=open('c:/data/names-after-re.txt','r')
for line in list_of_words: 
        #print line    
        data.append(line)                    
f.close()



for line in list_of_words:
 
    try:
        k=(list(itertools.combinations(line,2)))   #creating all possible two tuple name combinations of names that are in a picture 
        data_combo.append(k)
    
    except:   
        pass


# adding tuples of names (that appear in a picture together) as related nodes connected with an edge of weight 1. This creates a weieghted 
#undirected multigraph between the nodes. We use the 

M1 = nx.MultiGraph()
G1 = nx.Graph()

for line in data_combo:
    for node in line:
        try:                  
                M1.add_node(node[0])
                M1.add_node(node[1])
                M1.add_edge(node[0], node[1], weight = 1)
                
        except Exception, e:
            print str(e)
            pass


#this creates a graph with nodes and edges
w=0
bestfr=[]
name1=[]
name2=[]
wt=[]
for u,v,data in M1.edges_iter(data=True):
    w = data['weight']
    if G1.has_edge(u,v):
        G1[u][v]['weight'] += w
    else:
        G1.add_edge(u, v, weight=w)
for line in G1.edges(data=True):
    if (str(line[0])!='') and (str(line[0])!=''):        
        name1.append(str(line[0]))
        name2.append(str(line[1]))
        k=line[2].get('weight')
        wt.append(k)


#This creating a list of 3 elements (name1,name2,weight of the edges between these names)
name_wt=zip(name1,name2,wt)


# Sort the list by the 3rd element, i.e. weight
edgesortall=[]
edgesortall = sorted(name_wt,key=lambda x:(x[2]), reverse=True)


#check if the list of sorted names works
for line in edgesort1000:
    for word in line:
        print word


# To save the ouptout as a csv file
import csv
with open("c:/data/outputgraph.csv", "wb") as final:
    writer = csv.writer(final)
    writer.writerows(edgesortall)


#to find the number of times a name appears we ouput the number of names and degrees
nod=[]
deg=[]
for line in M1.nodes():
      nod.append(str(line))
      deg.append(M1.degree(line))
final=zip(nod,deg)


final1=final
final1 = filter(None, final1)
import re
final_list=[]
finalnames=[]
final100sort=[]
for line in final1:        
            finalnames.append(line)
        
final100sort= sorted(finalnames,key=lambda x:(x[1]), reverse=True)
print final100sort


# To save the ouput of the number of times a name appears as a csv file
import csv
with open("c:/data/outputgraphbypopularity.csv", "wb") as final:
    writer = csv.writer(final)
    writer.writerows(final100sort)


#function to sort the number of edges between different nodes
edgesort100=[]
edgesort100 = sorted(nameswt,key=lambda x:(x[1]), reverse=True)[:100]
print edgesort100


#to create pagerank of the names using pagerank from networkx library
pgrank=[]
pgsortall=[]
import operator
pgrank=nx.pagerank(G1)
pgsortall = sorted(pgrank.items(), key=operator.itemgetter(1), reverse=True)


# To save the pagerank output as a csv file
import csv
with open("c:/data/outputgraphpagerank.csv", "wb") as final:
    writer = csv.writer(final)
    writer.writerows(pgsortall)

