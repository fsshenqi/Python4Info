# -*- coding: utf-8 -*-
import json
import urllib
import urllib2

host_url = "http://apis.baidu.com/apistore/pullword/words?"

#address = raw_input('Enter location: ')
url = host_url + urllib.urlencode({"source": "佛山市魁奇路东延线二期工程", "param1": 0.5, "param2": 1})
req = urllib2.Request(url)
req.add_header("apikey", "")

print 'Retrieving', url
uh = urllib2.urlopen(req)
data = uh.read()
print 'Retrieved',len(data),'characters'
print data.decode("utf8").encode("gbk")
result_file = open("result.txt", "wb")
result_file.write(data)
result_file.close()


