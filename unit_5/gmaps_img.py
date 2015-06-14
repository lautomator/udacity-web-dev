from collections import namedtuple

# make a basic Point class
Point = namedtuple('Point', ["lat", "lon"])
points = [Point(1,2),
          Point(3,4),
          Point(5,6)]

# implement the function gmaps_img(points) that returns the google maps image
# for a map with the points passed in. A example valid response looks like
# this:
#
# http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&markers=1,2&markers=3,4
#
# Note that you should be able to get the first and second part of an individual Point p with
# p.lat and p.lon, respectively, based on the above code. For example, points[0].lat would 
# return 1, while points[2].lon would return 6.

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"

#def gmaps_img(points):
    
#    markers = []
#    marker = "markers="
    
    # extract the coords from the list of points    
#    for p in points:
#        markers.append(marker + str(p.lat) + "," + str(p.lon) + "&")
    
#    url = GMAPS_URL + ''.join(markers).strip('&')

#    return url



# his solution:

def gmaps_img(points):
    
    markers = '&'.join('markers=%s,%s' % (p.lat, p.lon)
                            for p in points)
    
    url = GMAPS_URL + markers
    
    return url

print gmaps_img(points)

