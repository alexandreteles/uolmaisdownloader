from inc import parser
import easygui
import sys

class cgui:
	def __init__(self):
		try:
			inputfile = self.inputdialog()
			if not inputfile:
				easygui.msgbox("Este programa nao pode continuar sem um arquivo de links. Por favor, tente novamente.")
				return None
			outputpath = self.outputdialog()
			if not outputpath:
				easygui.msgbox("Este programa nao pode continuar sem um diretorio de saida. Por favor, tente novamente.")
				return None
			ismeta = self.ismetadialog()
			if not ismeta:
				easygui.msgbox("Este programa nao pode continuar sem um arquivo de links. Por favor, tente novamente.")
				return None
			elif ismeta == "Gerar arquivo de metalinks":
				try:
					try:
						parse = parser.parser()
						parse.metalinkfile(inputfile, outputpath, easygui.filesavebox(), True)
					except:
						easygui.msgbox("Nao foi possivel gerar o arquivo de metalinks. Por favor, tente novamente.")
						self.errordialog()
						return None	
				except:
					easygui.msgbox("Nao foi possivel gerar o arquivo de metalinks. Por favor, tente novamente.")
					self.errordialog()
					return None
			else:
				downloadmethod = self.downloadmethoddialog()
				if not downloadmethod:
					easygui.msgbox("Este programa nao pode continuar sem um metodo de download. Por favor, tente novamente.")
					return None
				elif downloadmethod == "Simples":
					self.simpledownloaddialog()
					return None
				else:
					self.aria2downloaddialog()
					return None
		except:
			return None
	def inputdialog(self):
		inputdialog = "Na proxima janela, por favor, selecione o arquivo com os links para download."
		inputtitle = "Seja bem vindo ao UOL Mais Downloader"
		if easygui.ccbox(inputdialog, inputtitle):
			try:
				inputfile = easygui.fileopenbox()
				return inputfile
			except:
				easygui.msgbox("Houve um problema ao processar o arquivo de links. Voce clicou em cancelar, o arquivo e invalido ou possui permissoes incorretas.")
				self.errordialog()
		else:
			return False
	def errordialog(self):
		errordialog = "Voce deseja ver a excecao gerada?"
		errortitle = "ERRO"
		if easygui.ccbox(errordialog, errortitle):
			easygui.exceptionbox()
			return False
		else:
			return False
	def outputdialog(self):
		outputdialog = "Na proxima janela, por favor, selecione o diretorio destino."
		outputtitle = "Seja bem vindo ao UOL Mais Downloader"
		if easygui.ccbox(outputdialog, outputtitle):
			try:
				outputdir = easygui.diropenbox()
				return outputdir
			except:
				easygui.msgbox("Houve um problema ao processar o diretorio de destino. Voce clicou em cancelar, o diretorio e invalido ou possui permissoes incorretas.")
				self.errordialog()
				sys.exit(0)
		else:
			print "Este programa nao pode continuar sem um diretorio de saida. Por favor, tente novamente."
			return False
	def downloadmethoddialog(self):
		easygui.msgbox("Na proxima janela, por favor, selecione o metodo de dowload.")
		msg ="Selecione o metodo de download:"
		title = "METODO DE DOWNLOAD"
		choices = ["Simples", "Aria2"]
		try:
			choice = easygui.choicebox(msg, title, choices)
			return choice
		except:
			easygui.msgbox("Houve um problema ao processar a escolha do metodo de download.")
			self.errordialog()
			return False
	def ismetadialog(self):
		easygui.msgbox("Na proxima janela, por favor, informe se voce deseja gerar um arquivo de metalinks ou efetuar download.")
		msg ="Gerar arquivo de metalinks ou efetuar download?"
		title = "Gerar arquivo de metalinks ou efetuar download?"
		choices = ["Gerar arquivo de metalinks", "Efetuar download"]
		try:
			choice = easygui.choicebox(msg, title, choices)
			return choice
		except:
			easygui.msgbox("Houve um problema ao processar a escolha da funcao do aplicativo.")
			self.errordialog()
			return False