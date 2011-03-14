"""
dspacejira.py - Jenni Jira Module
Author: Peter Dietz
About: http://inamidst.com/phenny/

This module will paste the title and full url to an issue in jira when it recognizes the ticket number.
"""

import re
import urllib2
from htmlentitydefs import name2codepoint
import web

jira_finder = re.compile(r'((DS|ds)(-\d+))')

def show_dspacejira(jenni, input):
    try:
        results = get_results(input)
    except: return
    if results is None: return

    for r in results:
        jenni.say('[ %s ] - %s' % (r[0], r[1]))
show_dspacejira.rule = '.*((DS|ds)(-\d+)).*'
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
            page_title = find_title(page_url)
        except:
            page_title = None # if it can't access the site fail silently

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

def find_title(url):
    """
    This finds the title when provided with a string of a URL. It returns "
    """
    uri = url

    if not re.search('^((https?)|(ftp))://', uri):
        uri = 'http://' + uri

    redirects = 0
    while True:
        req = urllib2.Request(uri, headers={'Accept':'text/html'})
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.8) Gecko/20100722')
        u = urllib2.urlopen(req)
        info = u.info()
        u.close()

        if not isinstance(info, list):
            status = '200'
        else:
            status = str(info[1])
            info = info[0]
        if status.startswith('3'):
            uri = urlparse.urljoin(uri, info['Location'])
        else: break

        redirects += 1
        if redirects >= 50:
            return "Too many re-directs."

    try: mtype = info['content-type']
    except:
        return 
    if not (('/html' in mtype) or ('/xhtml' in mtype)):
        return 

    u = urllib2.urlopen(req)
    bytes = u.read(262144)
    u.close()

    content = bytes
    regex = re.compile('<(/?)title( [^>]+)?>', re.IGNORECASE)
    content = regex.sub(r'<\1title>',content)
    regex = re.compile('[\'"]<title>[\'"]', re.IGNORECASE)
    content = regex.sub('',content)
    start = content.find('<title>')
    if start == -1: return INVALID_WEBSITE
    end = content.find('</title>', start)
    if end == -1: return
    content = content[start+7:end]
    content = content.strip('\n').rstrip().lstrip()
    title = content

    if len(title) > 200:
        title = title[:200] + '[...]'

    def e(m):
        entity = m.group()
        if entity.startswith('&#x'):
            cp = int(entity[3:-1],16)
            return unichr(cp).encode('utf-8')
        elif entity.startswith('&#'):
            cp = int(entity[2:-1])
            return unichr(cp).encode('utf-8')
        else:
            char = name2codepoint[entity[1:-1]]
            return unichr(char).encode('utf-8')

    title = r_entity.sub(e, title)

    if title:
        try: title.decode('utf-8')
        except:
            try: title = title.decode('iso-8859-1').encode('utf-8')
            except: title = title.decode('cp1252').encode('utf-8')
        else: pass
    else: title = 'None'

    title = title.replace('\n', '')
    title = title.replace('\r', '')

    def remove_spaces(x):
        if "  " in x:
            x = x.replace("  ", " ")
            return remove_spaces(x)
        else:
            return x

    title = remove_spaces (title)

    if title:
        return title

if __name__ == '__main__':
    print __doc__.strip()
