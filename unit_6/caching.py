import time

# complex_computation() simulates a slow function. time.sleep(n) causes the
# program to pause for n seconds. In real life, this might be a call to a
# database, or a request to another web service.


def complex_computation(a, b):
    time.sleep(.5)
    return a + b


# QUIZ - Improve the cached_computation() function below so that it caches
# results after computing them for the first time so future calls are faster
cache = {(5, 3): 8}


def cached_computation(a, b):

    # check to see if this calculation exists
    for k in cache:
        if k == (a, b):
            print k.value()
        else:
            r = complex_computation(a, b)
            cache[(a, b)] = r
            return r


# test data
start_time = time.time()
print cached_computation(5, 3)
print "the first computation took %f seconds" % (time.time() - start_time)

start_time2 = time.time()
print cached_computation(5, 3)
print "the second computation took %f seconds" % (time.time() - start_time2)

# # other input
# start_time = time.time()
# print cached_computation(20, 3)
# print "the first computation took %f seconds" % (time.time() - start_time)

# start_time2 = time.time()
# print cached_computation(20, 3)
# print "the second computation took %f seconds" % (time.time() - start_time2)

print cache
