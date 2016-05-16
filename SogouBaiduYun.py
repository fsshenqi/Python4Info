
import urllib
from BeautifulSoup.BeautifulSoup import *
sample_url = "http://www.sogou.com/sogou?query=site%3Apan.baidu.com+%E7%81%AB%E9%94%85%E8%8B%B1%E9%9B%84&ie=utf8&num=100"
actual_url = "http://python-data.dr-chuck.net/known_by_Valerie.html"

# keyword = raw_input("Enter keyword: ")
# input_url = raw_input("Enter URL: ")
# input_count = raw_input("Enter count: ")

url = sample_url

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
tags = soup('a')
yun_links = [ a.get("href", None) for a in tags if a.get("name", None) == "dttl"]
print yun_links
