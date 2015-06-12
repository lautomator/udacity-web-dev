from xml.dom.minidom import parseString

# simple example of some example
s = """
<library>
    <book>Eugene Atget: Unknown Paris</book>
    <book>Lynn Davis Monument</book>
    <book>The Beat Reader</book>
</library>
"""

# parse the xml
p = parseString(s)

# make the xml tidy
print p.toprettyxml()

# print by the tag name and the child node
print p.getElementsByTagName("book")[0].childNodes[0].nodeValue
