#!/usr/bin/env python

import sys
import re
import requests
import scraperwiki

api_url = 'http://en.wikipedia.org/w/api.php?action=query&format=json' 
i = 0

def count_members(category):
    query = '&list=categorymembers&cmtitle=%s&cmsort=timestamp&cmdir=desc&cmlimit=max' % category
    request = requests.get(api_url + query)
    json_content = request.json()
    members = json_content['query']['categorymembers']

    for member in members:
        if 'Category:' in member['title']:
            count_members(member['title'])
        else:
            global i
            i = i + 1

def main():
    category = sys.argv[1].replace(' ', '_')
    
    n_list = count_members('Category:' + category)

    print i

if __name__ == '__main__': 
    main()
