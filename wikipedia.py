import requests
import json
import scraperwiki
import re

pageid = 37534696
api_url = 'http://en.wikipedia.org/w/api.php?' 

def clean_brackets(item):
    return re.sub('(\[\[)|(\]\])', '', item)

def clean_html(item):
    return re.sub('<[^<]+?>', '', item)

def scrape_members(category):
    query = 'action=query&list=categorymembers&cmtitle=%s&format=json&cmsort=timestamp&cmdir=desc&cmlimit=max' % category
    request = requests.get(api_url + query)
    json_content = request.json()
    data_list = []
    for member in json_content['query']['categorymembers']:
        print member['pageid']
        data = scrape_infobox(member['pageid'])
        if data != None:
            data_list.append(data)
    scraperwiki.sql.save(['id'], data_list)

def scrape_infobox(pageid):
    query = 'format=json&action=query&pageids=%s&prop=revisions&rvprop=content' % pageid
    request = requests.get(api_url + query)
    json_content = request.json()
    pageid = json_content['query']['pages'].keys()[0]
    content = json_content['query']['pages'][pageid]['revisions'][0]['*']
    article_name = json_content['query']['pages'][pageid]['title']    

    if 'infobox' not in content.lower():
        print 'Infobox not found for ' + article_name
        return None

    content = content[content.lower().find('{{infobox')::]
    content = content[:re.search('\n[^\n{]*\}\}[^\n{]*\n', content).start():]
    content = content.split('\n|')

    data = {}

    for item in content[1::]:
        if '=' in item:
            pair = item.split('=', 1)
            try:
                field = pair[0].strip()
                value = pair[1].strip()
                value = clean_brackets(value)
                value = clean_html(value)
                if field not in data.keys():
                    data[field] = value
                data['id'] = pageid
                data['article_name'] = article_name
            except IndexError:
                print 'IndexError!'
                exit(1)

    return data

def main():
    scrape_members('Category:Airports_in_England')

if __name__ == '__main__':
    main()

