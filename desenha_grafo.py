# -*-coding:utf-8 -*-
from grafo import Grafo
from reta import Reta
import math, time, random
import configuracao as cfg


class DesenhaGrafo():
    """
    Representa a interação entre a camada de interface (GUI) e a
    estrutura Grafo.
    """
    def __init__(self, canvas, callback):
        self.grafo = Grafo()
        self.canvas = canvas
        self.vertices = []	#coordenadas dos vértices
        self.arestas = []	#coordenadas das arestas
        self.selecionados = set()
        self.selecionadas = [] #TODO: mudar esse nome. Usada para arestas.
        self.attCallback(callback)
        self.desenhaGrafo()

    def attCallback(self, func):
        """Recebe a funcao opcoes(peso, label) para chamada nessa classe"""
        self.callback = func

    def getVerticePos(self, vertice):
        """Retorna as coordenadas do vertice do grafo"""
        return self.vertices[vertice]

    def setVerticePos(self, vertice, coordenadas):
        """Seta as coordenadas do vertice do grafo"""
        self.vertices[vertice] = coordenadas
        self.canvas.move('vertice', *coordenadas)
        self.canvas.update()

    def colideVerticeAresta(self, coord, raio, checaVertice = True):
        """Checa colisao entre o vertice(passado como parametro por meio das coordenadas e raio), os demais vertices e as arestas"""
        xca, yca, xcb, ycb = coord[0]-raio, coord[1]-raio, coord[0]+raio, coord[1]+raio
        if checaVertice:
            for x,y in self.vertices:
                xa, ya, xb, yb = x-raio, y-raio, x+raio, y+raio
                if xa <= xca <= xb and ya <= yca <= yb:
                    return (True,True)
                elif xa <= xcb <= xb and ya <= ycb <= yb:
                    return (True,True)
                elif xa <= xcb <= xb and ya <= yca <= yb:
                    return (True,True)
                elif xa <= xca <= xb and ya <= ycb <= yb:
                    return (True,True)

        #as quatros retas represetam o quadrado que envolve o vertice
        retaA = Reta((xca,yca,xcb,yca))
        retaB = Reta((xca,yca,xca,ycb))
        retaC = Reta((xcb,yca,xcb,ycb))
        retaD = Reta((xca,ycb,xcb,ycb))
        #################################################################
        for xra,yra,xrb,yrb,va,vb in self.arestas:
            #faz a checagem se houve algum cruzamento das retas
            retaX = Reta((xra,yra,xrb,yrb))
            if retaX.checaInter(retaA) or retaX.checaInter(retaB) or retaX.checaInter(retaC) or retaX.checaInter(retaD):
                return (True,va,vb)

        return (False,False)

    def colidePontoVertice(self, coord, raio):
        """Checa se um ponto colide com algum vertice do grafo, ele retorna o vertice que colodiu"""
        for n in range(len(self.vertices)):
            x, y = self.vertices[n][0], self.vertices[n][1]
            xa, ya, xb, yb = x-raio, y-raio, x+raio, y+raio
            if xa < coord[0] < xb and ya < coord[1] < yb:
                return n
        return -1

    def colidePontoAresta(self, coord, raio):
        """Checa se um ponto colide com alguma aresta do grafo"""
        for x,y in self.vertices:
            xca, yca, xcb, ycb = x-raio, y-raio, x+raio, y+raio
            retaA = Reta((xca,yca,xcb,yca))
            retaB = Reta((xca,yca,xca,ycb))
            retaC = Reta((xcb,yca,xcb,ycb))
            retaD = Reta((xca,ycb,xcb,ycb))
            retaX = Reta(coord)
            if retaX.checaInter(retaA) or retaX.checaInter(retaB) or retaX.checaInter(retaC) or retaX.checaInter(retaD):
                return True
        return False

    def desenhaVertice(self, coordenadas, label=None):
        """Cria um novo vertice e o printa na tela, caso nao colida com nenhum outro vertice ou uma aresta"""
        b = self.colideVerticeAresta(coordenadas, cfg.TAM_VERTICE)
        if not b[0]:
            self.grafo.addVertice(label)
            self.vertices.append(coordenadas)
            self.desenhaGrafo()
        else:
            print 'colidiu mah!!!'

    def apagaVertice(self, coordenadas):
        """Apaga o vertice que tem (x,y) =  coordenadas, caso exista tal vertice"""
        nvertice = self.colidePontoVertice(coordenadas, cfg.TAM_VERTICE)
        if nvertice > -1:
            self.grafo.remVertice(nvertice)
            del self.vertices[nvertice]
            self.desenhaGrafo()
        else:
            print 'nao colidiu mah!!!'

    def apagaAresta(self,coordenadas):
        """Apaga a aresta caso ela contenha (x,y) = coordenadas"""
        x,y = coordenadas
        b = self.colideVerticeAresta(coordenadas, cfg.TAM_VERTICE-20, False)
        if b[0]:
                self.grafo.remAresta((b[1],b[2]))
        self.desenhaGrafo()

    def selecionaVertice(self, coordenadas,peso = -1, dir = 0, add = True):
        """Seleciona um vertice. Se ja houver um outro vertice selecionado e o modo aresta estiver ativo uma nova aresta é feita
        entre os vertices selecionados"""
        nvertice = self.colidePontoVertice(coordenadas, cfg.TAM_VERTICE)
        if nvertice > -1:
            if nvertice not in self.selecionados:
                if len(self.selecionados) > 0:
                    if add ==  True:
                        aux = self.selecionados.pop()
                        self.grafo.addAresta((aux, nvertice),peso)
                        if dir == 0:
                            self.grafo.addAresta((nvertice, aux),peso)
                        nvertice = -1
                else:
                    self.selecionados.add(nvertice)
            else:
                self.selecionados.remove(nvertice)
                nvertice = -1
            self.desenhaGrafo()
        else:
            self.selecionados.clear()
            self.desenhaGrafo()
            print 'num selecionou ninguem!!!'
        return nvertice

    def moverTodos(self, posicao):
        """Move todo o grafo"""
        print posicao
        dx, dy = posicao
        for i, vertice in enumerate(self.vertices):
            self.vertices[i] = (vertice[0] + dx, vertice[1] + dy)
        print self.vertices
        self.desenhaGrafo()

    def buscaProfundidade(self, verticePos):
        """Chama o método de busca de pronfudidade do grafo e pisca os vertices passado por ele"""
        inicial = self.colidePontoVertice(verticePos, cfg.TAM_VERTICE)
        ordem = self.grafo.buscaProfundidade(inicial)
        self.animaGrafo(ordem,1.0)
        print ordem

    def buscaLargura(self, verticePos):
        """Chama o método de busca por largura do grafo e pisca os vertices passado por ele"""
        inicial = self.colidePontoVertice(verticePos, cfg.TAM_VERTICE)
        ordem = self.grafo.buscaLargura(inicial)
        self.animaGrafo(ordem,1.0)
        print ordem

    def agmPrim(self):
        """Chama a o metodo de prim do grafo e muda o cor das arestas da arvore geradora minima"""
        ordem = self.grafo.agmPrim()
        self.selecionadas.extend(ordem)
        self.desenhaGrafo()

    def agmKruskal(self):
        """Chama a o metodo de Kruskal do grafo e muda o cor das arestas da arvore geradora minima"""
        ordem = self.grafo.agmKruskal()
        print ordem
        self.selecionadas.extend(ordem)
        self.desenhaGrafo()

    def colorir(self):
        """Chama o metodo de coloracao do grafo e os colore na tela"""
        cores = self.grafo.colorir()
        self.coloreGrafo(cores)


    def _gerarCores(self, n):
        """Gera as coloracoe dos vertices"""
        print 'gerar', n, 'cores'
        lista = []
        i = 0
        repetir = False
        while i < n:
            repetir = False
            novacor = random.randint(0,255), random.randint(0,255), random.randint(0,255)
            print novacor
            for cor in lista:
                dif = abs(cor[0] - novacor[0]) + abs(cor[1] - novacor[1]) + abs(cor[2] - novacor[2])
                print dif,
                if dif < 20:
                    repetir = True
                    break
            if not repetir:
                lista.append(novacor)
                i += 1
        return lista


    def coloreGrafo(self, cores):
        """Faz a coloracao dos vertices"""
        ncores = max(cores)
        listaCores = self._gerarCores(ncores)
        for indice in range(len(self.vertices)):
            x, y = self.vertices[indice]
            self.circuloFull((x,y), cfg.TAM_VERTICE, str(indice), "#%02x%02x%02x" % listaCores[cores[indice]-1])


    def circuloFull(self, centro, raio, tag, ccor = None):
        """Cria um novo circulo de outra cor por cima dos vertices"""
        x, y = centro
        cor = cfg.COR_VERTICE
        gamb = int(tag)	#TODO: warning: gambiarra...
        if gamb in self.selecionados:
            cor = cfg.COR_SELECIONADA
        elif ccor is not None:
            cor = ccor
        self.canvas.create_oval(x-raio, y-raio, x+raio,y+raio, tag=tag, fill=cor,outline=cor, width=2)


    def minDijkstra(self,sour,dest):
        """Chama a o metodo de Dijkstra para menor caminho do grafo e muda o cor das arestas mostrando qual e esse caminho"""
        ordem = self.grafo.minDijkstra(sour,dest)
        print ordem
        self.selecionadas.extend(ordem)
        self.desenhaGrafo()

    def minBellman(self,sour,dest):
        """Chama a o metodo de Bellman para menor caminho do grafo e muda o cor das arestas mostrando qual e esse caminho"""
        ordem = self.grafo.minBellman(sour,dest)
        print ordem
        self.selecionadas.extend(ordem)
        self.desenhaGrafo()

    #TODO: refatorar essa funcao. Muitos parametros.
    def circulo(self, centro, raio, tag, ccor = None):
        """Desenha um circulo na tela"""
        x, y = centro
        cor = cfg.COR_VERTICE
        gamb = int(tag)	#TODO: warning: gambiarra...
        if gamb in self.selecionados:
            cor = cfg.COR_SELECIONADA
        elif ccor is not None:
            cor = ccor
        self.canvas.create_oval(x-raio, y-raio, x+raio,y+raio, tag=tag, outline=cor, width=2)

    def animaGrafo(self, lista, passo=cfg.ANM_PASSO):
        """Metódo que faz animacao nos metodos de busca"""
        self.selecionados.clear()
        self.desenhaGrafo()
        self.canvas.update()
        time.sleep(passo)
        back = -1
        for indice in lista:
            if back >= 0:
                self.circulo(self.vertices[back], cfg.TAM_VERTICE, str(indice),ccor=cfg.COR_ANIMACAO2)
                self.canvas.create_text(self.vertices[back],text=str(back),fill=cfg.COR_TEXTO1)
            self.circulo(self.vertices[indice], cfg.TAM_VERTICE, str(indice),ccor=cfg.COR_ANIMACAO1)
            self.canvas.create_text(self.vertices[indice],text=str(indice),fill=cfg.COR_TEXTO1)
            back = indice
            self.canvas.update()
            time.sleep(passo)
        time.sleep(passo)
        self.desenhaGrafo()

    def tremerGrafo(self):
        """Faz a tela tremer de um modo nao muito bonito"""
        y=10
        for x in range(1,20):
            self.canvas.move('all',x,y)
            self.canvas.update()
            time.sleep(0.1)
            self.canvas.move('all',-x,-y)
            self.canvas.update()
            y-=1
            time.sleep(0.1)
        for x in range(20,1,-1):
            self.canvas.move('all',x,y)
            self.canvas.update()
            time.sleep(0.1)
            self.canvas.move('all',-x,-y)
            self.canvas.update()
            time.sleep(0.1)
            y+=1

    def desenhaGrafo(self):
        """Faz todo o tratamento para reprintar todo o grafo na tela"""
        w,h = self.canvas["width"],self.canvas["height"]
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, w, h, fill=cfg.COR_TELA)
        self.arestas = []	#TODO: pensar se seria melhor fazer self.arestas[:] = []
        raio = cfg.TAM_VERTICE
        peso, direcao, label = self.callback()

        for indice in range(len(self.vertices)):
            x, y = self.vertices[indice]
            self.circulo((x,y), cfg.TAM_VERTICE, str(indice))
            if label == 0:
                self.canvas.create_text(self.vertices[indice],text=str(indice), tag = str(indice), activefill="#405252", fill=cfg.COR_TEXTO2)
            else:
                self.canvas.create_text(self.vertices[indice],text=self.grafo.labels[indice], tag = str(indice), activefill="#405252", fill=cfg.COR_TEXTO2)

        for va in range(len(self.grafo.matriz)):
            arestas = self.grafo.matriz[va]
            for vb, pesob in arestas:
                xa, ya = self.vertices[va]
                xb, yb = self.vertices[vb]
                #print pesob
                ang = math.atan2(xb-xa, yb-ya)
                ang2 = math.atan2(xa-xb, ya-yb)
                #print int(15*math.cos(ang)), int(15*math.sin(ang))
                if peso == 1:
                    self.canvas.create_text(((xb+xa)/2 + int(15*math.sin(ang+1.57)),
                        (ya+yb)/2 + int(15*math.cos(ang+1.57))), text=str(pesob),
                        tag = str(va)+'-'+str(vb), fill=cfg.COR_SELECIONADA)
                x, y = xa + raio * math.sin(ang), ya + raio * math.cos(ang)
                x2, y2 = xb + raio * math.sin(ang2), yb + raio * math.cos(ang2)
                cor = 'white'
                if (va, vb) in self.selecionadas or (vb, va) in self.selecionadas:
                    cor = cfg.COR_ARESTA2
                self.canvas.create_line(x,y,x2,y2, tag=str(va)+'-'+str(vb), fill=cor,width=2, arrow="last")
                self.arestas.append((x,y,x2,y2,va,vb))
        self.selecionadas = []

    def info(self):
        """Fornece informacoes sobre a estrutura."""
        info = []
        info.append(len(self.vertices))
        for a,b in self.vertices:
            info.append(a)
            info.append(b)
        info.extend(self.grafo.info())
        return info

    def carregar(self, info):
        """Carrega o grafo e desenha na tela"""
        indice, nvertices = 1, int(info[0])
        while (indice < 2 * nvertices + 1):
            self.vertices.append((int(info[indice]), int(info[indice+1])))
            indice += 2
        self.grafo.carregar(info[2 * nvertices + 1:])
        self.desenhaGrafo()
