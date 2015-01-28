from bs4 import BeautifulSoup # used to parse the HTML
from inc import downloader
import socket # used to set a connection timeout
import urllib2 # used to get the HTML resource from a URL
import string
import unicodedata
import os
import fileinput
import random

timeout = 60 # time in seconds
socket.setdefaulttimeout(timeout)

class parser:
	def randomstring(self, size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
		return ''.join(random.choice(chars) for _ in range(size))
	def url(self, link):
		httprequest = urllib2.Request(link)
		try:
			httpresponse = urllib2.urlopen(httprequest)
			pagesource = httpresponse.read()
		except URLError as e:
		    if hasattr(e, 'reason'):
		        print 'Servidor inacessivel.'
		        print 'Razao: ', e.reason
		        return False
		    elif hasattr(e, 'code'):
		        print 'O servidor nao pode processar a solicitacao.'
		        print 'Codigo de erro: ', e.code
		        return False
		else:
			return pagesource
	def html(self, pagesource):
		delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())

		objecttag_array = []
		swflink_array = []
		mediaid_array = []
		mediaid_clean_array = []
		return_array = []

		if pagesource == False:
			print "A pagina tem um codigo fonte invalido. Nao podemos trabalhar com este link!"
			return False
		else:
			try:
				del return_array[:] # make sure that we are workin in a empty array
				sourcecode = BeautifulSoup(pagesource)
			except:
				print "Houve um erro ao criar a arvore de objetos HTML. Nao podemos trabalhar com este link!"
				return False
		try:
			# get file id
			objecttag = str(sourcecode.find(property="og:video"))
			objecttag_array = objecttag.split(" ")
			swflink = objecttag_array[1]
			swflink_array = swflink.split("?")
			mediaid = swflink_array[1]
			mediaid_array = mediaid.split("&")
			mediaid_clean = mediaid_array[0]
			mediaid_clean_array = mediaid_clean.split("=")
			fileid = mediaid_clean_array[1]
			
			fileaddress = self.downloadlink(fileid)

			return_array.append(fileaddress)

			# get file name
			titletag = sourcecode.find(id="postTitle")
			titletag_content = titletag.contents
			title_unicode = unicode.join(u'\n',map(unicode,titletag_content)) # we need to get a unicode representation of the bs object
			title_string = unicodedata.normalize('NFKD', title_unicode).encode('ascii','ignore') # as unicode names isn't supported on all plataforms we will mangle it to ascii
			title = title_string.translate(None, delchars) # here we will delete all non alphanumeric char
			return_array.append(title.lower())

		except:
			print "Houve um erro ao processar o HTML da pagina. Nao podemos trabalhar com este link!"
			return False
		return return_array
	def downloadlink(self, fileid):
		if fileid == False:
			print "Impossivel obter o id do arquivo. Nao podemos trabalhar com este link!"
			return False
		else:
			try:
				fileaddress = "http://video31.mais.uol.com.br/" + fileid + ".mp4?r=http://player.mais.uol.com.br/player_video_v2.swf"
			except:
				print "Houve um erro ao criar o link de download. Nao podemos trabalhar com este link!"
				return False
		return fileaddress
	def metalinkfile(self, inputfile, outputpath, metafile, isgui="False"):
		aux = 1
		if not isgui:
			metafile = outputpath + metafile
			if os.path.isfile(metafile):
				while os.path.isfile(metafile):
					metafile = metafile + "." + self.randomstring()
		try:
			with open(metafile,'a') as metafile_object:
				for line in fileinput.input(inputfile):
					print "Analisando link numero: " + str(aux)
					print "URL Original: " + line
					try:
						download_array = self.html(self.url(line))
						print "URL de Download: " + download_array[0]
						print "Nome do Arquivo: " + download_array[1] + ".mp4\n"
						metafile_object.write(download_array[0] + "\n")
						metafile_object.write("\tout=" + download_array[1] + ".mp4\n")
						aux += 1
					except:
						print "Houve um erro ao processar a URL. Nao podemos trabalhar com este link."
						return False
			print "Processamento concluido."
			return metafile
		except:
			print "Houve um erro ao criar o arquivo de metalinks. Nao podemos trabalhar com este arquivo."
			return False
	def simpledownload(self, inputfile, outputpath):
		aux = 1
		download = downloader.downloader()
		for line in fileinput.input(inputfile):
			print "Baixando arquivo numero: " + str(aux)
			print "URL Original: " + line
			download_array = self.html(self.url(line))
			time_elapsed = download.file(download_array[0], download_array[1], outputpath)
			print "Download completo."
	  		print "Tempo total: " + str(time_elapsed)
			aux += 1
		print "Processamento concluido."
	def aria2cdownload(self, inputfile, outputpath, concurrency, aria2cpath):
		download = downloader.downloader()
		randomstring = self.randomstring()
		metafile_temp = "meta_temp." + randomstring
		metafile = self.metalinkfile(inputfile, outputpath, metafile_temp)
		download.aria2c(metafile, concurrency, outputpath, aria2cpath)
