import urllib2
from xml.dom.minidom import parseString

# source url
url = urllib2.urlopen(
    'http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml')

# read the content, this happens to be XML
page_content = url.read()

# store the content in a var
rss = parseString(page_content)

# store the 'items' in a list
items = rss.getElementsByTagName("item")

# tells me how many items
print len(items)
