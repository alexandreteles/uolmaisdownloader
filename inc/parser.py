from bs4 import BeautifulSoup # used to parse the HTML
import socket # used to set a connection timeout
import urllib2 # used to get the HTML resource from a URL
import string
import unicodedata

timeout = 60 # time in seconds
socket.setdefaulttimeout(timeout)

class parser:
	def url(self, link):
		httprequest = urllib2.Request(link)
		try:
			httpresponse = urllib2.urlopen(httprequest)
			pagesource = httpresponse.read()
		except URLError as e:
		    if hasattr(e, 'reason'):
		        print 'We failed to reach a server.'
		        print 'Reason: ', e.reason
		        return False
		    elif hasattr(e, 'code'):
		        print 'The server couldn\'t fulfill the request.'
		        print 'Error code: ', e.code
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
			print "The page has a invalid source code. We can't work with this link!"
			return False
		else:
			try:
				del return_array[:] # make sure that we are workin in a empty array
				sourcecode = BeautifulSoup(pagesource)
			except:
				print "There is a error when creating the HTML object tree. We can't work in this link!"
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
			print "There is a error when parsing the HTML provided by the page. We can't work in this link!"
			return False
		return return_array
	def downloadlink(self, fileid):
		if fileid == False:
			print "Impossible to obtain file id. We can't work in this link!"
			return False
		else:
			try:
				fileaddress = "http://video31.mais.uol.com.br/" + fileid + ".mp4?r=http://player.mais.uol.com.br/player_video_v2.swf"
			except:
				print "There is a problem when creating the download link. We can't work in this link!"
				return False
		return fileaddress