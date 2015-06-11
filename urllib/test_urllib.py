import urllib2

p = urllib2.urlopen('http://www.example.com')

c = p.read()

print c

print dir(p)

print p.headers

print p.headers.keys()
