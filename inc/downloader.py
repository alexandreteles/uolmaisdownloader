import socket # used to set a connection timeout
import sys
import urllib2
import os
import time

timeout = 60 # time in seconds
socket.setdefaulttimeout(timeout)

class downloader:
	def file(self, url, file_name, path): # from: https://gist.github.com/medigeek/3176958
		aux = 0

		clean_url = url.split("?")
		clean_url = clean_url[0]

		if os.path.isfile(file_name):
			file_name = path + file_name + "." + aux + ".mp4"
		else:
			file_name = path + file_name + ".mp4"

		req = urllib2.Request(url)
		req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0')
		
		u = urllib2.urlopen(req)
		f = open(file_name, 'wb')
		meta = u.info()

		print "File destination: " + file_name

		file_size = int(meta.getheaders("Content-Length")[0])

		if file_size < 1000:
			unity = "Byte(s)"
		elif file_size >= 1000 and file_size < 1000000:
			unity = "Kilobyte(s)"
			print_size = file_size / 1000
		elif file_size >= 1000000 and file_size < 1000000000:
			unity = "Megabyte(s)"
			print_size = file_size / 1000000
		elif file_size >= 1000000000:
			unity = "Gigabyte(s)"
			print_size = file_size / 1000000000

		print("Downloading from: {0} ( Size: {1} {2} )".format(clean_url, print_size, unity))

		file_size_dl = 0
		block_sz = 8192
		starttime = time.clock()
		while True:
		    buffer = u.read(block_sz)
		    if not buffer:
		        break

		    file_size_dl += len(buffer)
		    f.write(buffer)
		    p = float(file_size_dl) / file_size
		    #status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
		    #status = status + chr(8)*(len(status)+1)
		    done = int(50 * file_size_dl / file_size)
		    sys.stdout.write("\r[%s%s] %s kbps" % ('=' * done, ' ' * (50-done), (file_size_dl//(time.clock() - starttime)/1000)))
		    #sys.stdout.write(status)

		f.close()
		enlapsedtime = time.clock() - starttime
		aux += 1

		return enlapsedtime