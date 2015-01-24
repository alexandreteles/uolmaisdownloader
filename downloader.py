#!/bin/python

from inc import parser
from inc import downloader
import argparse
import fileinput
import os

argparser = argparse.ArgumentParser()
argparser.add_argument("inputfile", help="file from where we will read the links")
argparser.add_argument("outputpath", help="path where files will be stored")
args = argparser.parse_args()

inputfile = args.inputfile
outputpath = args.outputpath

download_array = []

if os.path.isfile(inputfile) and os.path.isdir(outputpath):
	parse = parser.parser()
	download = downloader.downloader()
	aux = 1
	for line in fileinput.input(inputfile):
		del download_array[:]
		print "Downloading file file number: " + str(aux)
		print "Original URL: " + line
		download_array = parse.html(parse.url(line))
		time_elapsed = download.file(download_array[0], download_array[1], outputpath)
		print "Download complete."
  		print "Time Elapsed: " + str(time_elapsed)
		aux += 1
elif not os.path.isfile(inputfile):
	print "The input file doesn't exist or have wrong permissions."
if not os.path.isdir(outputpath):
	print "The outputpath doesn't exist or have wrong permissions."