#!/bin/python

from inc import parser
import argparse
import os

argparser = argparse.ArgumentParser()
argparser.add_argument("arquivoentrada", nargs=1, help="caminho para o arquivo contendo os links para download")
argparser.add_argument("diretoriodestino", nargs=1, help="caminho para o diretorio destino dos arquivos baixados")
argparser.add_argument("--criarmeta", help="cria um arquivo de metalinks para download com o aria2 no diretorio de saida. nao efetua nenhum dowload.", action='store_true')
argparser.add_argument("--arquivometa", help="nome do arquivo de metalinks a ser salvo no diretorio destino (valido somente se usado com '--meta').")
argparser.add_argument("--usararia2", help="define se o aria2 sera utilizado para download (usado para downloads concorrentes).", action='store_true')
argparser.add_argument("--aria2c", nargs=1, help="caminho para o binario do aria2, usado para downloads concorrentes. valido somente se usado com '--usararia2').")
argparser.add_argument("--emparalelo", nargs=1, default=5, help="numero de downloads concorrents. padrao = 5 (valido soment se usado com '--aria2c').")
argparser.add_argument("--versao", action="version", version="Software: %(prog)s | Versao: git-testing", help="imprime a versao do programa")

args = argparser.parse_args()

## Arguments

# <list> variables
inputfile = args.arquivoentrada[0]
outputpath = args.diretoriodestino[0]

# <string> variables
metafile = args.arquivometa
if not type(args.aria2c).__name__ == "NoneType":
	aria2cpath = args.aria2c[0]

# <boolean> variables
ismeta = args.criarmeta
usearia2 = args.usararia2

# <integer> variables
if type(args.emparalelo).__name__ == "list":
	concurrency = args.emparalelo[0]
	concurrency = int(concurrency)
else:
	concurrency = args.emparalelo

if os.path.isfile(inputfile) and os.path.isdir(outputpath):
	parse = parser.parser()
	aux = 1
	if not ismeta:
		if not usearia2:
			parse.simpledownload(inputfile, outputpath)
		else:
			parse.aria2cdownload(inputfile, outputpath, concurrency, aria2cpath)
	else:
		parse.metalinkfile(inputfile, outputpath, metafile)
elif not os.path.isfile(inputfile):
	print "O arquivo de entrada nao existe ou tem as permissoes erradas."
if not os.path.isdir(outputpath):
	print "O diretorio destino nao existe ou tem as permissoes erradas."
