import socket
import re

file_url = "http://www.pythonlearn.com/code/urllinks.py"

host = re.findall("http://(\S+?)/", file_url)[0]
filename = re.findall("/([^/]+?)$", file_url)[0]

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect((host, 80))
mysock.send('GET ' + file_url + ' HTTP/1.0\n\n')

count = 0
picture = "";
while True:
    data = mysock.recv(5120)
    data_len = len(data)
    if (data_len < 1) : break
    count = count + data_len
    picture = picture + data
    print data_len, count

mysock.close()
pos = picture.find('\r\n\r\n')
print 'Header length',pos
print(picture[:pos])

picture = picture[pos+4:]
fhand = open(filename, "wb")
fhand.write(picture)
fhand.close()
