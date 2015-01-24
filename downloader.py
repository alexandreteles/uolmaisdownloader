#!/bin/python

from inc import parser
from inc import downloader
import argparse
import fileinput
import os

argparser = argparse.ArgumentParser()
argparser.add_argument("arquivoentrada", nargs=1, help="caminho para o arquivo contendo os links para download")
argparser.add_argument("diretoriodestino", nargs=1, help="caminho para o diretorio destino dos arquivos baixados")
argparser.add_argument("-m, --meta", help="cria um arquivo de metalinks para download com o aria2 no diretorio de saida. nao efetua nenhum dowload.", action='store_true')
argparser.add_argument("--arquivometa", help="nome do arquivo de metalinks a ser salvo no diretorio destino (valido somente se usado com '--meta')")
argparser.add_argument("--aria2c", nargs=1, help="caminho para o binario do aria2 (usado para downloads concorrentes)")
argparser.add_argument("-n", "--emparalelo", nargs=1, default=5, help="numero de downloads concorrents. padrao = 5 (valido soment se usado com '--aria2c'")
argparser.add_argument("-v", "--versao", action="version", version="Software: %(prog)s | Versao: git-testing", help="imprime a versao do programa")

args = argparser.parse_args()

inputfile = args.inputfile
outputpath = args.outputpath
ismeta = args.meta

download_array = []

if os.path.isfile(inputfile) and os.path.isdir(outputpath):
	parse = parser.parser()
	aux = 1
	if not ismeta:
		download = downloader.downloader()
		for line in fileinput.input(inputfile):
			del download_array[:]
			print "Baixando arquivo numero: " + str(aux)
			print "URL Original: " + line
			download_array = parse.html(parse.url(line))
			time_elapsed = download.file(download_array[0], download_array[1], outputpath)
			print "Download completo."
	  		print "Tempo total: " + str(time_elapsed)
			aux += 1
	else:
		filecount = -1
		metafile = outputpath + metafile
		if os.path.isfile(metafile):
			while os.path.isfile(metafile):
				filecount += 1
				metafile = metafile + filecount
		for line in fileinput.input(inputfile):
			del download_array[:]
			print "Analisando link numero: " + str(aux)
			print "URL Original: " + line
			download_array = parse.html(parse.url(line))
			time_elapsed = download.file(download_array[0], download_array[1], outputpath)
			aux += 1
elif not os.path.isfile(inputfile):
	print "O arquivo de entrada nao existe ou tem as permissoes erradas."
if not os.path.isdir(outputpath):
	print "O diretorio destino nao existe ou tem as permissoes erradas."
