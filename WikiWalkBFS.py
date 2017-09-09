'''
WalkWiki.py
Written by Thomas Besenski
Sept 9th 2017
finds the shortest path between 2 wikipedia articles specified in the cmd line args.
an edge exists from article A to article B if there exists a hyperlink within article A that 
leads to article B.

takes 2 command line arguments, which are the starting URL extension and the ending URL extension.
These arguments represent the text which comes after "en.wikipedia.org/wiki/" on a wikipedia article,
'''
from queue import *
import datetime
import random
import urllib.request
import re
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import sys
"""
getResponse function will return an HTTPResponse object from the parameter url
"""
def getResponse(url):
    try: 
        #print ("url =  " +url)
        response = urllib.request.urlopen(url)
        #DEBUG SHIT
        #print ("This is the url of the html file we requested: " + url)
        #print ("this is the url of the response reached: " + response.geturl())
        return response
    except HTTPError as e:
        print (e)
        return None
'''
getValidWiki(outputList, wikiResponse)
outputList: the list of links found from the wiki article pages
wikiResponse: the HTTPResponse object from which we make a BS4 object out of to parse 
'''
def getValidWikiLinks(outputList, wikiResponse):
    
    
    #i used this pattern from the textbook, Web Scraping in Python by Ryan Mitchell
	
    wikiArticlePattern = r'^(/wiki/)((?!:).)*$'
    soup = BeautifulSoup(wikiResponse, 'html.parser')
    #make the wikiarticlepattern into a Pattern object
    pattern = re.compile(wikiArticlePattern)
    for link in soup.findAll("a"):
        if "href" in link.attrs:
            if (pattern.match(link.attrs['href'])!= None):
                outputList.append(link.attrs["href"])
            
    return
'''
main(currentURL, finishURL)
pseudocode



add the currentURL to an empty Queue
create a hashmap which stores keys of an article's name and elements which is the article which lead to it (parent relationship in graph)

while the Queue is not empty:

   -find all links in the front article
    during this, if the destination link is found, follow the hashmap "trail"
     (which is organized as such: (key = <child> : element = <parent>)), to return to 
     the root URL 'startingURL'
     break the loop and return an ordered list of the articles passed through to reach
     the finalURL defined by the user.
        
   -for all the links in the front article:
        if the link is a key in the hashmap, then it has already been visited, so continue
        if the link is not a key in the hashmap, then add the url to the queue to be scanned
        continue
    
'''
    
def main(startingURL, finishURL):
    #QUEUE TO RUN THE BFS for the finishURL
    q = Queue(0)
    #DICTIONARY TO FIND THE TRAIL LEADING BACKWARDS
    trail = {}
    #defining the currentURL outside of the while loop to retain the position
    currentURL = ""
    #place the starting url into the queue to be processed
    q.put(startingURL)
    wikiArticleLinks = []
    #loop will continue until there are no links to articles that havent been explored yet
    
    
    attempts = 0
    #UNCOMMENT TO DEBUG 
    print("Attempting to find: " + finishURL+ " from " + startingURL)
    while not q.empty():
        attempts++
        if (attempts == 1000):
            print("Scanned 1000 articles, did not find destination")
            quit()
    #   get the head of the queue, 
        currentURL = q.get()
        response = getResponse("https://en.wikipedia.org" + currentURL)
        wikiArticleLinks.clear()
        getValidWikiLinks(wikiArticleLinks, response)   

     #shows where we are in search
        print ("Wikipedia Article: " + currentURL+ ",  Article Links Found: " + str(len(wikiArticleLinks)))
    
        if (finishURL) in (wikiArticleLinks):
            print ("\nfound!!!")
            print("found the URL: " + finishURL + " in the article: " + currentURL)
            break
        #this is the situation where the url is not found and articles are added to the queue to be scanned
        else:
            for link in wikiArticleLinks:
                if link not in trail:
                    trail[link]= currentURL
                    q.put(link)
    
    
    
    
    s= []
    while (currentURL!= startingURL):
        s.append(currentURL) 
        
        #Debugging purposes only
        #print("the element for " + currentURL + " in \"trail\" is " + str(trail[currentURL]))
        currentURL = trail[currentURL]
     
        
    s.append(finishURL)
    temp = [startingURL]
    print (temp + s)
    
 
    

    
    
    return 

# this is where the main function is invoked, and the command line arguments are used
if (len(sys.argv)<3):
    print("Needs 2 command line argument")
    quit()
commandLineArgument1 = str(sys.argv[1])
commandLineArgument2 = str(sys.argv[2])
main("/wiki/" + commandLineArgument1,"/wiki/" + commandLineArgument2)
