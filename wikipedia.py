import requests
import json
import scraperwiki

query = 'format=json&action=query&titles=ScraperWiki&prop=revisions&rvprop=content'
request = requests.get('http://en.wikipedia.org/w/api.php?' + query)
pageid = request.json()['query']['pages'].keys()[0]
content = request.json()['query']['pages'][pageid]['revisions'][0]['*']

scraperwiki.sql.execute("create table if not exists swdata (field, value)")

content = content.split('\n|')

content[-1] = content[-1][:content[-1].find('\n'):]

for item in content[1::]:
    pair = item[1::].split('=')
    try:
        field = pair[0].strip()
        value = pair[1].strip()
        print field, value
        scraperwiki.sql.execute("insert into swdata values('%s', '%s')" % (field, value))
    except IndexError:
        print 'IndexError!'

scraperwiki.sql.commit()