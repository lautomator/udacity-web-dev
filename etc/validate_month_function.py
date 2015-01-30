months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
    ]

# dictionary with the first 3 letters (key) and month (value):
months_abbv = dict((m[:3].lower(), m) for m in months)


def valid_month(month):

    if month:
        short_month = month[:3].lower()
        return months_abbv.get(short_month)

# original version
# def valid_month(month):
#
#    cap_month = month.capitalize()
#
#    for m in months:
#        if cap_month == m:
#            return cap_month

print valid_month("january")
# => "January"
print valid_month("January")
# => "January"
print valid_month("foo")
# => None
print valid_month("")
# => None
print valid_month("febrUary")
print valid_month("octOBER")
print valid_month("Oct")
print valid_month("oct4323f$#$d")
