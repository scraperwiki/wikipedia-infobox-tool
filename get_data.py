#!/usr/bin/env python

import sys
import json
import re
import requests
import scraperwiki

api_url = 'http://en.wikipedia.org/w/api.php?action=query&format=json' 

def clean_brackets(item):
    return re.sub('(\[\[)|(\]\])', '', item)

def clean_html(item):
    return re.sub('<[^<]+?>', '', item)

def get_data_list(members):
    data_list = []
    for member in members:
        if 'Category:' in member['title']:
            scrape_members(member['title']) 
        else:
            #print "Scraping infobox for '%s'" % member['title']
            data = scrape_infobox(member['pageid'])
            if data != None and len(data) > 0:
                data_list.append(data)
                #print "Scraping done for '%s'" % member['title']
    return data_list

def scrape_members(category):
    category = category.replace(' ', '_')
    query = '&list=categorymembers&cmtitle=Category:%s&cmsort=timestamp&cmdir=desc&cmlimit=max' % category
    print query
    request = requests.get(api_url + query)
    json_content = request.json()
    data_list = get_data_list(json_content['query']['categorymembers'])
    if len(data_list) > 0:
        scraperwiki.sql.save(['id'], data_list)

def scrape_infobox(pageid):
    query = '&action=query&pageids=%s&prop=revisions&rvprop=content' % pageid
    request = requests.get(api_url + query)
    json_content = request.json()
    pageid = json_content['query']['pages'].keys()[0]
    content = json_content['query']['pages'][pageid]['revisions'][0]['*']
    article_name = json_content['query']['pages'][pageid]['title']    

    if 'infobox' in content.lower():
        content = content[content.lower().find('{{infobox')::]
    elif 'taxobox' in content.lower():
        content = content[content.lower().find('{{taxobox')::]
    else:
        #print "Infobox not found for '%s'" % article_name
        return None

    infobox_end = re.search('\n[^\n{]*\}\}[^\n{]*\n', content)

    if infobox_end == None:
        #print "Closing tag not found for '%s'" % article_name
        return None

    content = content[:infobox_end.start():]
    content = re.split('\n[^|]\|', content)

    data = {}

    for item in content[1::]:
        if '=' in item:
            pair = item.split('=', 1)
            try:
                field = pair[0].strip()
                value = pair[1].strip()
                value = clean_brackets(value)
                value = clean_html(value)
                data[field.lower()] = value
                data['id'] = pageid
                data['article_name'] = article_name
            except IndexError:
                print 'IndexError!'
                exit(1)

    return data

def main():
    print sys.argv[1]
    scrape_members(sys.argv[1])
    print 'Success!'

if __name__ == '__main__':
    main()

