#import subprocess
import pexpect
import socket # used to set a connection timeout
import sys
import urllib2
import os
import time

timeout = 60 # time in seconds
socket.setdefaulttimeout(timeout)

class downloader:
	def file(self, url, file_name, path): # from: https://gist.github.com/medigeek/3176958
		try:
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

			print "Arquivo de destino: " + file_name

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

			print("Baixando da URL: {0} ( Tamanho: {1} {2} )".format(clean_url, print_size, unity))

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
				done = int(50 * file_size_dl / file_size)
				sys.stdout.write("\r[%s%s] %s Kbps" % ('=' * done, ' ' * (50-done), (file_size_dl//(time.clock() - starttime)/1024)))

			f.close()
			enlapsedtime = time.clock() - starttime
			aux += 1
			return enlapsedtime
		except:
			print "Nao foi possivel efetuar o download deste arquivo. Nao podemos trabalhar com este link!"
	def aria2c(self, metalink_file, concurrency, outputpath, aria2cpath):
		#aria2carguments = " --user-agent='Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0' -i " + str(metalink_file) + " -d " + str(outputpath) + " -j " + str(concurrency) + " -c"
		aria2carguments = ["-i",
							str(metalink_file),
							"-d",
							str(outputpath),
							"-j",
							str(concurrency),
							"--user-agent='Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'",
							"--split=5",
							"--file-allocation=falloc",
							"--enable-http-pipelining=true",
							"--console-log-level=notice",
							"--max-connection-per-server=10",
							"--min-split-size=5M",
							"--summary-interval=60",
							"--stream-piece-selector=geom",
							"-c"]
		#aria2c = aria2cpath + aria2carguments
		#print "Linha de comando aria2c: " + aria2c
		try:
			#proc = subprocess.Popen(aria2c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			proc = pexpect.spawn(aria2cpath, aria2carguments, maxread=1, timeout=None, logfile=sys.stdout)
			for line in proc:
				print line,
			proc.close()

			# while True:
			# 	out = proc.stderr.read(1)
			# 	if out == '' and proc.poll() != None:
			# 		break
			# 	if out != '':
			# 		sys.stdout.write(out)
			# 		sys.stdout.flush()
			return True
		except:
			print "Impossivel iniciar ou completar o download. Verifique o caminho para o binario aria2c ou os links providos para download."
			return False