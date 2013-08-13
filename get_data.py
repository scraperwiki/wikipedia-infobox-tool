#!/usr/bin/env python

import sys
import json
import re
import requests
import scraperwiki

api_url = 'http://en.wikipedia.org/w/api.php?action=query&format=json' 

def clean_data(data):
    data = re.sub('(\[\[)|(\]\])', '', data)
    data = re.sub('<[^<]+?>', '', data) 
    return data

def scrape_members(category):
    def get_data_list(members, category):
        data_list = []
        pages = []
        subcategories = []
        for member in members:
            if 'Category:' in member['title']:
                subcategories.append(member['title'])
            else:
                pages.append(member['pageid']) 
        for page in pages:
            data = scrape_infobox(page)
            if data != None and len(data) > 0:
                data_list.append(data)
        print 'Scraped %s of %s pages in %s' % (len(data_list), len(pages), category)
        for subcategory in subcategories:
            scrape_members(subcategory.replace('Category:', '')) 
        return data_list

    category = category.replace(' ', '_')
    query = '&list=categorymembers&cmtitle=Category:%s&cmsort=timestamp&cmdir=desc&cmlimit=max' % category
    request = requests.get(api_url + query)
    json_content = request.json()
    members = json_content['query']['categorymembers'] 
    data_list = get_data_list(members, category)
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
        return None

    infobox_end = re.search('\n[^\n{]*\}\}[^\n{]*\n', content)

    if infobox_end == None:
        return None

    content = content[:infobox_end.start():]
    content = re.split('\n[^|\n]*\|', content)

    data = {}

    for item in content[1::]:
        if '=' in item:
            pair = item.split('=', 1)
            field = pair[0].strip()
            value = pair[1].strip()
            value = clean_data(value)
            data[field.lower()] = value
            data['id'] = pageid
            data['article_name'] = article_name

    return data

def main():
    scraperwiki.sql.execute("drop table if exists swdata;")
    scraperwiki.sql.commit()  
    scrape_members(sys.argv[1])

if __name__ == '__main__':
    main()

