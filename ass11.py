
import urllib
from BeautifulSoup.BeautifulSoup import *
sample_url = "http://python-data.dr-chuck.net/comments_42.html"
actual_url = "http://python-data.dr-chuck.net/comments_275205.html"

url = actual_url
html = urllib.urlopen(url).read()

soup = BeautifulSoup(html)

# Retrieve all of the anchor tags
tags = soup('span')
print sum([int(tag.contents[0]) for tag in tags  if tag.get("class",None) == 'comments'])
