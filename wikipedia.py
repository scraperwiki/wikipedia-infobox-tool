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
    query = 'action=query&list=categorymembers&cmtitle=%s&format=json&cmsort=timestamp&cmdir=desc' % category
    request = requests.get(api_url + query)
    json_content = request.json()
    data_list = []
    for member in json_content['query']['categorymembers']:
        data_list.append(scrape_infobox(member['pageid']))
    scraperwiki.sql.save(['id'], data_list)

def scrape_infobox(pageid):
    query = 'format=json&action=query&pageids=%s&prop=revisions&rvprop=content' % pageid
    request = requests.get(api_url + query)
    json_content = request.json()
    pageid = json_content['query']['pages'].keys()[0]
    content = json_content['query']['pages'][pageid]['revisions'][0]['*']
    article_name = json_content['query']['pages'][pageid]['title']    

    content = content[:re.search('\n.*\}\}', content).start():]
    content = content.split('\n|')

    data = {}

    for item in content[1::]:
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
    scrape_members('Category:Recipients_of_the_Order_of_the_Seraphim')

if __name__ == '__main__':
    main()

