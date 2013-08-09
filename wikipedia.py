import requests
import json
import scraperwiki
import re

pageid = 37534696

def clean_brackets(item):
    return re.sub('(\[\[)|(\]\])', '', item)

def clean_html(item):
    return re.sub('<[^<]+?>', '', item)

def scrape_infobox(pageid):
    query = 'format=json&action=query&pageids=%s&prop=revisions&rvprop=content' % pageid
    request = requests.get('http://en.wikipedia.org/w/api.php?' + query)
    json_content = request.json()
    pageid = json_content['query']['pages'].keys()[0]
    content = json_content['query']['pages'][pageid]['revisions'][0]['*']
    article_name = json_content['query']['pages'][pageid]['title']    

    content = content.split('\n|')

    content[-1] = content[-1][:content[-1].find('\n'):]

    data = {}

    for item in content[1::]:
        pair = item.split('=', 1)
        try:
            field = pair[0].strip()
            value = pair[1].strip()
            value = clean_brackets(value)
            value = clean_html(value)
            data[field] = value
            data['Article Name'] = article_name
        except IndexError:
            print 'IndexError!'

    scraperwiki.sql.save(['Article Name'], data)

def main():
    scrape_infobox(pageid)

if __name__ == '__main__':
    main()

