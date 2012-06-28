"""
dspacejira.py - Jenni Jira Module
Author: Peter Dietz
About: http://inamidst.com/phenny/

This module will paste the title and full url to an issue in jira when it recognizes the ticket number.

Prereq: BeautifulSoup
To install BS, download it from the creator, and type 'python setup.py install' in the directory.
"""
import sys

import re
import BeautifulSoup
import urllib

projectList = 'APTRUST|aptrust|AKUBRA|akubra|HYGALL|hygall|DS|ds|DSB|dsb|DSCR|dscr|DSRV|dsrv|DWMVC|dwmvc|'
projectList += 'DURACLOUD|duracloud|CLOUDSYNC|cloudsync|FEDORACREATE|fedoracreate|FCREPO|fcrepo|HYDRA|hydra|'
projectList += 'HYARG|hyarg|HYHULL|hyhull|HYPAT|hypat|HYNDVID|hyndvid|HYLIBRA|hylibra|HYDRACAMP|hydracamp|'
projectList += 'HYDRNGA|hygranga|HYDRUS|hydrus|ISLANDORA|islandora|MURADORA|muradora|SANDBOX|sandbox|FUNAPI|funapi'



jira_finder = re.compile(r'((' + projectList  + ')(-\d+))')

def show_dspacejira(jenni, input):
    try:
        results = get_results(input)
    except:
        return

    if results is None: return

    for r in results:
        jenni.say('[ %s ] - %s' % (r[0], r[1]))
        show_dspacejira.rule = '.*((' + projectList + ')(-\d+)).*'
        show_dspacejira.priority = 'high'

def get_results(text):
    a = re.findall(jira_finder, text)
    k = len(a)
    i = 0
    display = [ ]
    while i < k:
        ticketID = str(a[i][0])
        page_url = find_url(ticketID)
        try:
            page_title = get_title(page_url)
        except:
            #page_title = "ehh"
            page_title = "Unexpected error:", sys.exc_info()[0] # if it can't access the site fail silentlyexcept:

        #display.append([page_title, page_url])
        display.append([page_url, page_title])
        i += 1
    return display

def find_url(ticketID):
    """
    This produces the jira issue URL
    """
    uri = 'https://jira.duraspace.org/browse/' + ticketID
    print uri
    return uri

def get_title(url):
    print url
    output = BeautifulSoup.BeautifulSoup(urllib.urlopen(url))
    print output.title.string
    return output.title.string
