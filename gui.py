#-*-coding: utf-8-*-
from Tkinter import *
import tkFileDialog as fDialog
from tkMessageBox import askquestion, showwarning

import os
import json

from desenhaGrafo import DesenhaGrafo


class MainWindow(object):
	"""
	Representa a janela principal do aplicativo. Esta classe se comunica com
	desenhaGrafo que por sua vez se comunica com o grafo propriamente dito.
	"""
	def __init__(self, raiz):
		#variáveis representando o comportamento da janela
		self.raiz = raiz
		self.status = -1
		self.isMove = False
		
		self.selecionado = -1
		self.mousePos = (0,0)	
		self.modificado = False

		#menu principal
		self.frameMenu = Frame(raiz, borderwidth = 2, relief = GROOVE)
		self.frameMenu.pack(fill=X, expand=True)

		
		self.menu = Menu(self.frameMenu)
		self.raiz.config(menu = self.menu)
		
		self.menuArquivo = Menu(self.menu)
		self.menu.add_cascade(label="Arquivo", menu=self.menuArquivo)
		self.menuArquivo.add_command(label="Novo", command=self.novo)
		self.menuArquivo.add_command(label="Carregar", command=self.carregar)
		self.menuArquivo.add_command(label="Salvar", command=self.salvar)
		self.menuArquivo.add_command(label="Sair", command=self.sair)

		self.menuConfiguracao = Menu(self.menu)
		self.menu.add_cascade(label="Configurar", menu=self.menuConfiguracao)
		self.menuConfiguracao.add_command(label='Prefer\xc3\xaancias', command=self.configurarAparencia)
		#self.menuArquivo.add_command(label="Carregar", command=self.carregar)
		#self.menuArquivo.add_command(label="Salvar", command=self.salvar)
		#self.menuArquivo.add_command(label="Sair", command=self.sair)"""

		#barra de opções
		self.frameOpcoes = Frame(raiz, borderwidth = 2)
		self.checaLabel = IntVar()
		Checkbutton(self.frameOpcoes, text="Label", variable=self.checaLabel).pack(side=LEFT)
		self.checaPeso = IntVar()
		Checkbutton(self.frameOpcoes, text="Pesos", variable=self.checaPeso).pack(side=LEFT)
		self.checaDirecionado = IntVar()
		Checkbutton(self.frameOpcoes, text="Direcionado", variable=self.checaDirecionado).pack()
		self.frameOpcoes.pack()
		
		#barra de atalhos
		self.frameAcoes = Frame(raiz)
		self.imVertice = PhotoImage(file = os.path.join(os.getcwd(),"img","vertice.gif"))
		self.imAresta = PhotoImage(file = os.path.join(os.getcwd(),"img","aresta.gif"))
		self.imMover = PhotoImage(file = os.path.join(os.getcwd(),"img","mover.gif"))
		self.imRemover = PhotoImage(file = os.path.join(os.getcwd(),"img","remover.gif"))
		self.imBfs = PhotoImage(file = os.path.join(os.getcwd(),"img","bfs.gif"))
		self.imDfs = PhotoImage(file = os.path.join(os.getcwd(),"img","dfs.gif"))
		self.imSmile = PhotoImage(file = os.path.join(os.getcwd(),"img","smile.gif"))
		self.imDijkstra = PhotoImage(file = os.path.join(os.getcwd(),"img","dijkstra.gif"))
		self.imBellman = PhotoImage(file = os.path.join(os.getcwd(),"img","bellman.gif"))
		self.imExclama = PhotoImage(file = os.path.join(os.getcwd(),"img","exclama.gif"))
		self.imPrim = PhotoImage(file = os.path.join(os.getcwd(),"img","agmprim.gif"))
		self.imKruskal = PhotoImage(file = os.path.join(os.getcwd(),"img","agmkruskal.gif"))
		self.imCor = PhotoImage(file = os.path.join(os.getcwd(),"img","cor.gif"))
		
		self.buttons = []
		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imVertice, justify=LEFT, command=lambda:self.atualizaEstado(0)))
		self.buttons[0].grid(row=0, column=0)

		self.buttons.append(Button(self.frameAcoes, width=50, height=50,image=self.imAresta, justify=LEFT,command=lambda:self.atualizaEstado(1)))
		self.buttons[1].grid(row=0, column=1)

		self.buttons.append(Button(self.frameAcoes, width=50, height=50,image=self.imMover, justify=LEFT, command=lambda:self.atualizaEstado(2)))
		self.buttons[2].grid(row=0, column=2)

		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imRemover, justify=LEFT, command=lambda:self.atualizaEstado(3)))
		self.buttons[3].grid(row=0, column=3)		
				
		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imBfs, justify=LEFT, command=lambda:self.atualizaEstado(4)))
		self.buttons[4].grid(row=0, column=4)	
		
		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imDfs, justify=LEFT, command=lambda:self.atualizaEstado(5)))
		self.buttons[5].grid(row=0, column=5)
		
		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imDijkstra, justify=LEFT, command=lambda:self.atualizaEstado(6)))
		self.buttons[6].grid(row=0, column=6)
		
		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imBellman, justify=LEFT, command=lambda:self.atualizaEstado(7)))
		self.buttons[7].grid(row=0, column=7)

		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imPrim, justify=LEFT, command=lambda:self.atualizaEstado(8)))
		self.buttons[8].grid(row=0, column=8)

		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imKruskal, justify=LEFT, command=lambda:self.atualizaEstado(9)))
		self.buttons[9].grid(row=0, column=9)		
		
		self.buttons.append(Button(self.frameAcoes, width=50, height=50, image=self.imCor, justify=LEFT, command=lambda:self.atualizaEstado(10)))
		self.buttons[10].grid(row=0, column=10)	
		self.frameAcoes.pack()
	
		#Canvas
		self.frameCanvas = Frame(raiz, borderwidth = 2)
		self.frameCanvas.pack()		

		self.canvas = Canvas(self.frameCanvas,  height=480, width = 720, highlightthickness=2)
		self.canvas.pack()

		#bindings
		self.canvas.bind("<Button-1>", self.checaclick)
		self.canvas.bind("<Motion>",self.atualizaPos)
		self.raiz.bind_all("<Up>", lambda foo:self.atualizaPos(foo, (0,-8)))
		self.raiz.bind_all("<Right>", lambda foo:self.atualizaPos(foo, (8,0)))
		self.raiz.bind_all("<Down>", lambda foo:self.atualizaPos(foo, (0,8)))
		self.raiz.bind_all("<Left>", lambda foo:self.atualizaPos(foo, (-8,0)))
		
		#desenhar grafo
		#ponto de conexão entre as camadas GUI e Desenho.
		self.desenho = DesenhaGrafo(self.canvas, self.opcoes)
		
	
	def opcoes(self):
		"""Método para ser usado como callback para obter o valor das opcoes(peso, label)"""
		return self.checaPeso.get(), self.checaDirecionado.get(), self.checaLabel.get()
		
	
	def obterInformacao(self, evento, mensagem):
		"""Chama a classe CaixaEntrada."""
		d = CaixaEntrada(self.raiz, evento, mensagem)
		self.raiz.wait_window(d.top)
		return d.get()
		
	def atualizaPos(self,event, direcao=None):
		"""Atualiza a posição do mouse."""
		if self.status == 2:
			if self.selecionado != -1:
				self.desenho.setVerticePos(self.selecionado,(event.x,event.y))
				self.desenho.desenhaGrafo()					
			elif direcao != None:
				self.desenho.moverTodos(direcao)

		
	def checaclick(self, evento):
		"""Método que trata da interação com o mouse."""
		if self.status == 0:
			label = None
			if self.checaLabel.get() == 1:
				label = self.obterInformacao(evento, 'Label')
			self.desenho.desenhaVertice((evento.x, evento.y), label)
		elif self.status == 1:
			if self.selecionado != -1:
				peso = 0
				direcionado = self.checaDirecionado.get() 
				if self.checaPeso.get() == 1: 
					peso = self.obterInformacao(evento, 'Peso')
				self.selecionado = (self.desenho.selecionaVertice((evento.x, evento.y),int(peso), dir = direcionado))
			else:
				self.selecionado = (self.desenho.selecionaVertice((evento.x, evento.y)))
		elif self.status == 2:
			self.selecionado = (self.desenho.selecionaVertice((evento.x, evento.y)))
		elif self.status == 3:
			self.desenho.apagaVertice((evento.x, evento.y))
			self.desenho.apagaAresta((evento.x,evento.y))
		elif self.status == 4:
			self.buscaLargura(evento)
		elif self.status == 5:
			self.buscaProfundidade(evento)
		elif self.status == 6:
			if self.selecionado == -1:
				self.selecionado = self.desenho.selecionaVertice((evento.x,evento.y),add = False)
			else:
				segundoSelecionado = self.desenho.selecionaVertice((evento.x,evento.y), add = False)
				if segundoSelecionado != -1:
					self.minDijkstra(self.selecionado,segundoSelecionado)
				else:
					self.selecionado = -1
		elif self.status == 7:
			if self.selecionado == -1:
				self.selecionado = self.desenho.selecionaVertice((evento.x,evento.y),add = False)
			else:
				segundoSelecionado = self.desenho.selecionaVertice((evento.x,evento.y), add = False)
				if segundoSelecionado != -1:
					self.minBellman(self.selecionado,segundoSelecionado)
				else:
					self.selecionado = -1
		elif self.status == 8:
			self.agmPrim(evento)
		elif self.status == 9:
			self.agmKruskal(evento)
		elif self.status == 10:
			self.colorir(evento)
		self.modificado = True
	
		
	def buscaProfundidade(self, evento):
		"""Chama a busca em profundidade da classe Desenho."""
		self.desenho.buscaProfundidade((evento.x, evento.y))
		
	def buscaLargura(self, evento):
		"""Chama a busca em largura da classe Desenho."""
		self.desenho.buscaLargura((evento.x, evento.y))
		
	def agmPrim(self, evento):
		"""Chama a AGM Prim da classe Desenho."""
		self.desenho.agmPrim()
		
	def agmKruskal(self,evento):
		"""Chama a AGM Kruskal da classe Desenho."""
		self.desenho.agmKruskal()
	
	def minDijkstra(self, origem, destino):
		"""Chama a Dijkstra da classe Desenho."""
		self.desenho.minDijkstra(origem, destino)
		
	def minBellman(self, origem, destino):
		"""Chama a Bellman-Ford da classe Desenho."""
		self.desenho.minBellman(origem, destino)
	
	def colorir(self,evento):
		"""Chama o método de coloração de grafos da classe Desenho."""
		self.desenho.colorir()
		
	def atualizaEstado(self,valor):
		"""Coordena o estado dos botões."""
		if self.status != -1:
			self.buttons[self.status].config(relief = RAISED)
		if valor != self.status:
			self.buttons[valor].config(relief = SUNKEN)
			self.status = valor
		else:
			self.status = -1	
		
	def carregar(self):
		"""Diálogo de abertura de arquivo."""
		arquivo = fDialog.askopenfile(parent=self.raiz,filetypes=[('grafo','*.grafo')],title='Carregar...')
		if arquivo != None:
			data = arquivo.read().split()
			self.desenho = DesenhaGrafo(self.canvas,self.opcoes)
			self.desenho.carregar(data)
			#print 'data: ', data
			arquivo.close()
	
	def salvar(self):
		"""Diálogo de salvamento de arquivo."""
		nomeArq = fDialog.asksaveasfilename(parent=self.raiz, filetypes=[('grafo','*.grafo')], title='Salvar...')
		if len(nomeArq) > 0:
			if not '.grafo' in nomeArq:
				nomeArq += '.grafo'
			#print nomeArq
			arquivo = open(nomeArq, "w")
			info = self.desenho.info()
			for x in info:
				arquivo.write(str(x) + ' ')
			arquivo.close()
			self.modificado = False
		else:
			showwarning( "Atencao", "O arquivo nao foi salvo!!!")
			
	def novo(self):
		"""Criar um novo arquivo. Checa se o grafo atual foi editado."""
		if self.modificado:
			yesOrNo = askquestion("","Salvar o grafo atual?")
			if yesOrNo == "yes":
				self.salvar()

		self.desenho = DesenhaGrafo(self.canvas, self.opcoes)

	def sair(self):
		"""Sair do programa. Checa se o grafo atual foi editado."""
		if self.modificado:
			yesOrNo = askquestion("","Salvar antes de sair?")
			if yesOrNo == "yes":
				self.salvar()

		self.raiz.quit()

	def configurarAparencia(self):
		JanelaConfiguracao(self.raiz)
	
	def exclama(self, evento):
		"""Método experimental. Inútil para o trabalho."""
		self.desenho.tremerGrafo()
	
	def foo(self, evento):
		"""Método utilizado em testes"""
		print 'foo', evento


class CaixaEntrada:
	"""
	Representa a caixa de entrada de dados. Pesos e Labels.
	"""
	def __init__(self, raiz, event, mensagem):
		self.top = Toplevel(raiz)
		self.top.geometry('+%d+%d' % (event.x_root, event.y_root - 30))
		#TODO: .geometry deveria se posicionar de acordo com a aresta...
		self.top.transient(raiz)	#janela sem maximizar e minimizar
			
		Label(self.top, text=mensagem).pack()
		self.e = Entry(self.top)
		self.e.pack(padx=5)
		self.value = 0

		b = Button(self.top, text="OK", command=self.ok)
		b.pack(pady=5)
	
	def ok(self):
		self.value = self.e.get()
		self.top.destroy()

	def get(self):
		return self.value


"""    def color(self):
        rgb, hx = tkColorChooser.askcolor("white")
        print rgb, hx
        self.parent.config(bg=hx)"""

class JanelaConfiguracao:
	def __init__ (self, raiz):
		self.raiz = Toplevel(raiz)
		
		arq1 = open('configuracao.js', 'r')
		configuracao = json.loads(arq1.read())
		arq1.close()
		#print configuracao

		self.frameQtde = Frame(self.raiz)
		self.frameQtde.pack()

		self.lbQtde = Label(self.frameQtde, text = "Quantidade de Testes:")
		self.lbQtde.pack(padx=3, side=LEFT)

		self.scQtde = Scale(self.frameQtde, from_=1, to=1000, orient=HORIZONTAL, resolution=25, length=250)
		self.scQtde.pack()

		self.frameAgente = Frame(self.raiz)
		self.frameAgente.pack()

		self.lbAgente = Label(self.frameAgente, text = "Tipo de Agente:")
		self.lbAgente.pack(padx=3, side=LEFT)

		tipos = [("Reativo Simples", 1),("Estado Interno", 2), ("Busca 1", 3), ("Busca 2", 4)]

		self.tipoAgente = IntVar()

		for texto, tipo in tipos:
			Radiobutton(self.frameAgente, text=texto, variable=self.tipoAgente, value=tipo).pack(side=LEFT, anchor=CENTER)

		self.tipoAgente.set(1)	
		
		self.frameCenario = Frame(self.raiz)
		self.frameCenario.pack()

		self.lbCenario = Label(self.frameCenario, text = "Cen\xe1rio utilizado:")
		self.lbCenario.pack(padx=3, side=LEFT)

		self.btCenario = Button(self.frameCenario, text="...", anchor=CENTER, justify=LEFT, command=self.carregar)
		self.btCenario.pack(padx=2, side=LEFT)

		self.caminho = StringVar()
		self.caminho.set("<especifique o arquivo>")

		self.lbCaminho = Label(self.frameCenario, textvariable = self.caminho)
		self.lbCaminho.pack(padx=2, side=LEFT)

		self.frameParada = Frame(self.raiz)
		self.frameParada.pack()

		self.lbParada = Label(self.frameParada, text = "Condi\xe7\xe3o de parada:")
		self.lbParada.pack(padx=3, side=LEFT)

		tipos = [("Itera\xe7\xf5es", 1),("Sujeira", 2)]

		self.tipoParada = IntVar()

		for texto, tipo in tipos:
			Radiobutton(self.frameParada, text=texto, variable=self.tipoParada, value=tipo).pack(side=LEFT, anchor=CENTER)	
	
		self.tipoParada.set(1)
		
		self.scParada = Scale(self.frameParada, from_=1, to=200, orient=HORIZONTAL, length=180)
		self.scParada.pack()
		
		self.dados = None

		self.btTestes = Button(self.raiz, text="Executar Testes!", anchor=CENTER, justify=LEFT, command=self.executar)
		self.btTestes.pack(padx=2)

		
	def carregar (self):
		nome, self.cenario = self.metodos.carregarArquivo(self.raiz)
		self.caminho.set(nome)
		
	def executar (self):
		self.controle = controle.Controle(self.cenario, self.tipoAgente.get())
		arq1 = open('config.js', 'r')
		config = json.loads(arq1.read())
		arq1.close()
		config['agente'] = self.tipoAgente.get()
		config['parada'] = self.tipoParada.get()	
		config['passos'] = self.scParada.get()
		config['sujeira'] = self.scParada.get()
		arq1 = open('config.js', 'w')
		arq1.write(json.dumps(config))
		arq1.close()
		self.controle.teste(self.scQtde.get())
