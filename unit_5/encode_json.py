import json


# a list of dictionaries
# requires:
# ---------
# content
# created
# last_modified
# subject

# only content and subject will be checked

# for email header set the content type correctly:
# Content-Type: application/json; charset=UTF-8

content = r'This is a \ < > } { test.'
subject = r'Test'
created = "Mon June 15, 2015 FPO"  # will need to make a function for this
# last_modified is the same as created because
# the blog does not have a feature for updating and entry
last_modified = "Mon June 15, 2015 FPO"  # same as created

j = json.dumps([{'content': content,
                 'subject': subject,
                 'created': created,
                 'last_modified': last_modified}])

print j
