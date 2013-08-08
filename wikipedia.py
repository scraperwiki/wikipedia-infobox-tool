import requests
import json
import scraperwiki

query = 'format=json&action=query&titles=ScraperWiki&prop=revisions&rvprop=content'
request = requests.get('http://en.wikipedia.org/w/api.php?' + query)
pageid = request.json()['query']['pages'].keys()[0]
content = request.json()['query']['pages'][pageid]['revisions'][0]['*']
#infobox = content[content.find('{{Infobox')::]
#infobox = infobox[:infobox.find('/n}}'):]

data = {
    'fieldName': [],
    'fieldValue': []
}
keys = []
values = []

content = content.split('\n|')

for item in content[1:-1:]:
    pair = item[1::].split('=')
    try:
        field = pair[0].strip()
        value = pair[1].strip()
        print field, value
        scraperwiki.sql.execute("insert into table swdata values(
    except IndexError:
        print 'IndexError!'

data['fieldName'] = keys
data['fieldValue'] = values
print type(data['fieldName'])
print type(data['fieldValue'])
scraperwiki.sql.save(['fieldName'], data)
