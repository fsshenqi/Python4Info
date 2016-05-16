
import urllib
from BeautifulSoup.BeautifulSoup import *
sample_url = "http://python-data.dr-chuck.net/known_by_Fikret.html"
actual_url = "http://python-data.dr-chuck.net/known_by_Valerie.html"

input_url = raw_input("Enter URL: ")
input_count = raw_input("Enter count: ")
input_position = raw_input("Enter position: ")

url = input_url
count = int(input_count)
position = int(input_position)

def find_name(cur_url):
    html = urllib.urlopen(cur_url).read()
    soup = BeautifulSoup(html)
    tags = soup('a')
    next_url = tags[position-1].get("href", None)
    return next_url

for i in range(count+1):
    print "Retrieving:",url
    url = find_name(url)
