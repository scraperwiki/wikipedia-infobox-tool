import requests
import json
import scraperwiki

query = 'format=json&action=query&titles=ScraperWiki&prop=revisions&rvprop=content'
request = requests.get('http://en.wikipedia.org/w/api.php?' + query)
pageid = request.json()['query']['pages'].keys()[0]
content = request.json()['query']['pages'][pageid]['revisions'][0]['*']

content = content.split('\n|')

content[-1] = content[-1][:content[-1].find('\n'):]

data = {}

for item in content[1::]:
    pair = item[1::].split('=')
    try:
        field = pair[0].strip()
        value = pair[1].strip()
        print field, value
        data[field] = value
        data['id'] = 0
    except IndexError:
        print 'IndexError!'

scraperwiki.sql.save(['id'], data)
