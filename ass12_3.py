
import urllib
from xml.etree import ElementTree
sample_url = "http://python-data.dr-chuck.net/comments_42.xml"
actual_url = "http://python-data.dr-chuck.net/comments_275202.xml"

input_url = raw_input("Enter location: ")

url = input_url
count = 0
total = 0

xml_file = urllib.urlopen(url)
print "Retrieving",url
xml_string = xml_file.read()
print "Retrieved", len(xml_string), "characters"
xml_tree = ElementTree.fromstring(xml_string)
comments = xml_tree.findall('.//comment')
print "Count:", len(comments)
counts = xml_tree.findall('.//count')
total = sum([ int(c.text) for c in counts])
print "Sum:", total
