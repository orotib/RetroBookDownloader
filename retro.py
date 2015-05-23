#!/usr/bin/env python
#!encoding: utf-8

"""
Retro Book Downloader

A simple python script for downloading retro books from pcvilag.muskatli.hu.

All books on this website: http://pcvilag.muskatli.hu/

Written by Tibor Oros, 2015 (oros.tibor0@gmail.com)

Recommended version: Python 2.7
"""

import os
import shutil
import sys
import urllib
import urllib2

from bs4 import BeautifulSoup

FOLDERNAME = 'temp'

def makeDir(name):
    if not(os.path.exists(name)):
        os.mkdir(name)
        os.chdir(name)
    else:
        shutil.rmtree(name)
        os.mkdir(name)
        os.chdir(name)
        
def getProjectName(url):
    return url.split('/')[5]

def makeLinkURL(mainUrl, projectName):
    return mainUrl + projectName + '/link.php'

def makeDownloadURL(mainUrl, projectName):
    return mainUrl + projectName + '/'

def getLinkName(link):
    return link.get('href').split('=')[1]

def openURL(linkUrl):
    tmp = urllib2.urlopen(linkUrl)
    soup = BeautifulSoup(tmp)
    return soup.find_all('a')

def downloadImages(links, downloadURL, errorItem):
    for link in links:
        if len(link.get('href').split('=')) == 2:
            try:
                pName = getLinkName(link)
                urllib.urlretrieve(downloadURL + pName, pName)
                print 'Downloaded image: ' + pName
            except IOError:
                print 'Image does not exist: ' + pName
                errorItem.append(pName)
            except:
                print 'Unknown error'
    
def deleteDir(name):
    os.chdir('..')
    shutil.rmtree(name)

def errorTest(ei):
    if len(ei) != 0:
        print '--- Missing image(s) ---'
        for i in ei:
            print i 


def main():
    mainURL = 'http://pcvilag.muskatli.hu/irodalom/cbooks/' 
    URL = raw_input('Book URL: ')
    
    try:
        projectName = getProjectName(URL)
        linkURL = makeLinkURL(mainURL, projectName)
        downloadURL = makeDownloadURL(mainURL, projectName)
        links = openURL(linkURL)
    except (urllib2.URLError, IndexError):
        print '*** Wrong URL ***'
        print 'Example: http://pcvilag.muskatli.hu/irodalom/cbooks/njk64/njk64.html'
        sys.exit()
        
    makeDir(FOLDERNAME)
    errorItem = []

    print 'Program downloading...'
    downloadImages(links, downloadURL, errorItem)
    print 'Downloading complete.'
    
    print 'Program converting...'
    os.system('convert *.jpg ../' + projectName + '.pdf')
    print 'Converting complete.'
    
    deleteDir(FOLDERNAME)
    errorTest(errorItem)   
    
    raw_input('Press enter to exit.')
    
    
######################################################
    
if __name__ == '__main__':
    main()
