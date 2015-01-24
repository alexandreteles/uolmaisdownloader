#!/bin/python

from inc import parser
from inc import downloader
import argparse
import fileinput
import os

argparser = argparse.ArgumentParser()
argparser.add_argument("arquivoentrada", nargs=1, help="caminho para o arquivo contendo os links para download")
argparser.add_argument("diretoriodestino", nargs=1, help="caminho para o diretorio destino dos arquivos baixados")
argparser.add_argument("--criarmeta", help="cria um arquivo de metalinks para download com o aria2 no diretorio de saida. nao efetua nenhum dowload.", action='store_true')
argparser.add_argument("--arquivometa", help="nome do arquivo de metalinks a ser salvo no diretorio destino (valido somente se usado com '--meta')")
argparser.add_argument("--usararia2", help="caminho para o binario do aria2 (usado para downloads concorrentes)", action='store_true')
argparser.add_argument("--aria2c", nargs=1, help="caminho para o binario do aria2 (usado para downloads concorrentes. valido somente se usado com '--usearia2')")
argparser.add_argument("--emparalelo", nargs=1, default=5, help="numero de downloads concorrents. padrao = 5 (valido soment se usado com '--aria2c'")
argparser.add_argument("--versao", action="version", version="Software: %(prog)s | Versao: git-testing", help="imprime a versao do programa")

args = argparser.parse_args()

inputfile = args.arquivoentrada[0]
outputpath = args.diretoriodestino[0]
ismeta = args.criarmeta
metafile = args.arquivometa

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
		print "Toda a lista foi processada."
	else:
		filecount = -1
		metafile = outputpath + metafile
		if os.path.isfile(metafile):
			while os.path.isfile(metafile):
				filecount += 1
				metafile = metafile + filecount
		with open(metafile,'a') as metafile_object:
			for line in fileinput.input(inputfile):
				del download_array[:]
				print "Analisando link numero: " + str(aux)
				print "URL Original: " + line
				download_array = parse.html(parse.url(line))
				metafile_object.write(download_array[0] + "\n")
				metafile_object.write("\tout=" + download_array[1] + ".mp4\n")
				aux += 1
		print "Toda a lista foi processada."
elif not os.path.isfile(inputfile):
	print "O arquivo de entrada nao existe ou tem as permissoes erradas."
if not os.path.isdir(outputpath):
	print "O diretorio destino nao existe ou tem as permissoes erradas."
