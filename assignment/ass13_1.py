import json
import urllib

input_url = raw_input("Enter location:")
file = urllib.urlopen(input_url)
print "Retrieving", input_url
json_read = json.loads(file.read())
print "Retrieved", len(json_read), "characters"
print "Count:", len(json_read["comments"])
print "Sum:", sum([ int(comment["count"]) for comment in json_read["comments"]])