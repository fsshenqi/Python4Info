import urllib

import re

while True:
    file_url = raw_input("Enter file URL:")
    if re.match("http://\S+[^/]$", file_url) : break
    else:
        print "It is not a file url!"

host = re.findall("http://(\S+?)/", file_url)[0]
filename = re.findall("/([^/]+?)$", file_url)[0]

webfile = urllib.urlopen(file_url)
local_file = open(filename, "wb")
size = 0
while True:
    piece = webfile.read(10000)
    if len(piece) < 1: break
    local_file.write(piece)
    size = size + len(piece)
local_file.close()
webfile.close()
print "URL:",file_url
print "File name:", filename
print size,'Bytes copied.'
