import urllib2

p = urllib2.urlopen('http://www.example.com')

c = p.read()

# print c

# print type(p)
# print dir(p)

print p.headers, '\n\n'

for key in p.headers.keys():
    print key

print '\n\n', p.headers['etag']

# print p.headers.keys()
