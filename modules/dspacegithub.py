# -*- coding: utf-8 -*-
"""
dspacegithub.py - Jenni GitHub Module
Author: Ivan Masár
About: http://inamidst.com/phenny/

This module will paste the title and full url to an GitHub pull request when it recognizes the PR number.

Prereq: BeautifulSoup
To install BS, download it from the creator, and type 'python setup.py install' in the directory.
"""
import sys

import re
import BeautifulSoup
import urllib

projectList = 'DSPR'

github_finder = re.compile(r'(('+projectList+')#(\d+))')

def show_dspacegithub(jenni, input):
    try:
        results = get_results(input)
    except:
        return

    if results is None: return

    for r in results:
        jenni.say('[ %s ] - %s' % (r[0], r[1]))
show_dspacegithub.rule = '.*(('+projectList+')#(\d+)).*'
show_dspacegithub.priority = 'high'

def get_results(text):
    matches = re.findall(github_finder, text)

    display = [ ]
    for match in matches:
        ticketID = str(match[0])
        page_url = find_url(match[2])
        try:
            page_title = get_title(page_url)
        except:
            page_title = "Unexpected error:", sys.exc_info()[0] # if it can't access the site fail silentlyexcept:

        display.append([page_url, page_title])
    return display

def find_url(ticketID):
    """
    This produces the GitHub PR URL
    """
    uri = 'https://github.com/DSpace/DSpace/pull/' + ticketID
    print uri
    return uri

def get_title(url):
    print url
    output = BeautifulSoup.BeautifulSoup(urllib.urlopen(url))
    s = output.title.string
    try:
        result = str(s[0:s.index("Pull Request")-2]) # cut the constant part that says " · Pull Request #123 · DSpace/DSpace · GitHub"
    except ValueError:
        result = output.title.string
    print result
    return result
