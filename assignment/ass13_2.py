import json
import urllib

host_url = "http://python-data.dr-chuck.net/geojson?"

address = raw_input('Enter location: ')

url = host_url + urllib.urlencode({'sensor':'false', 'address': address})
print 'Retrieving', url
uh = urllib.urlopen(url)
data = uh.read()
print 'Retrieved',len(data),'characters'

try: js = json.loads(str(data))
except: js = None
if not js or 'status' not in js or js['status'] != 'OK':
    print '==== Failure To Retrieve ===='
    print data

place_id = js["results"][0]["place_id"]
print "Place id", place_id

