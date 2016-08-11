# -*-coding:utf-8-*-
from heapMin import HeapMin, DijkstraNode

import configuracao as cfg
from list_ord import ListOrd


class Grafo(object):
    """
    Classe que modela a  estrutura de dados grafo
    """
    def __init__(self, bidirecional=False):
        self.matriz = []
        self.labels = []    #TODO: seria melhor 'matriz' ser uma tupla (listOdr, label)?
        self.bidirecional = bidirecional

    def addVertice(self, label=None):
        """adiciona um vertice ao grafo"""
        self.matriz.append(ListOrd())
        if label is None:
            self.labels.append(str(len(self.matriz)-1))
        else:
            self.labels.append(label)

    def remVertice(self,ver):
        """remove um vertice do grafo"""
        if ver >= len(self.matriz):#caso inválido
            return
        #com isso garantimos que o vertice existe e sera obrigatorio a reducao dos outros vertices
        #self._print()
        for i in range(len(self.matriz)):
            self.matriz[i].reduzir(ver) #apaga o elemento da lista e reduz os indices
        #self._print()
        del(self.matriz[ver]) #remove o vertice
        del(self.labels[ver]) #remove o label

    def addAresta(self,aresta, peso=-1):
        """adiciona uma aresta ao grafo"""
        va, vb = aresta
        if va < 0 or vb >= len(self.matriz):#caso invalido
            return
        self.matriz[va].add(vb, peso)
        if (self.bidirecional):
            self.matriz[vb].add(va, peso)

    def remAresta(self,aresta):
        """remove uma aresta do grafo"""
        va, vb = aresta
        if va < 0 or vb >= len(self.matriz):#caso invalido
            return
        print 'remAresta', va, vb
        self.matriz[va].remover(vb)
        if (self.bidirecional):
            self.matriz[vb].remover(va)

    def _print(self):
        """imprimi grafo no terminal"""
        for i in range(len(self.matriz)):
            print i,':',
            print self.matriz[i]
            print

    def info(self):
        """Retorna informacoes do grafo"""
        info = []
        info.append(len(self.matriz))
        for i in range(len(self.matriz)):
            info.append(len(self.matriz[i]))
            for vertice, peso in self.matriz[i]:
                info.append(vertice)
                info.append(peso)
        return info

    def carregar(self, info):
        """Carrega o grafo"""
        print '!', info
        nvertices, vertice, posicao = int(info[0]), 0, 1
        for i in range(nvertices):
            self.addVertice()
        while vertice  < nvertices:
            for i in range(int(info[posicao])):
                self.addAresta((vertice, int(info[posicao+1])), int(info[posicao+2]))
                posicao += 2
            posicao += 1
            vertice += 1
        self._print()

    def getPeso(self, vertice):
        """Retorna o peso entres vertices va,vb"""
        va, vb = vertice
        return self.matriz[va].getPeso(vb)

    def carregarMatriz(self, nomeArq):
        """Carrega matriz do grafo a partir de um arquivo"""
        arq = open(nomeArq,'r')
        linhas = arq.readlines()
        for k in range(len(linhas)):
            self.addVertice()
        for ini, linha in enumerate(linhas):
            elementos = linha.split()
            for fim, elemento in enumerate(elementos):
                print fim, elemento
                if elemento != '-' and elemento != ' ':
                    print 'adicionado', (ini, fim), int(elemento)
                    self.addAresta((ini, fim), int(elemento))
        self._print()

    def buscaProfundidade(self,pos = 0):
        """Implementacao do metodo de busca por profundidade"""
        visitados = [False for x in range(len(self.matriz))]
        ordem = []
        pilha = []
        pilha.append(pos)
        ordem.append(pos)
        visitados[pos] = True
        while len(pilha) > 0:
            pos = pilha[-1]
            for i, peso in self.matriz[pos]:
                if visitados[i] == False:
                    ordem.append(i)
                    visitados[i] = True
                    pilha.append(i)
                    break
            else:
                pilha.pop()
        return ordem

    def buscaLargura(self, pos = 0):
        """Implementaco do metodo de busca por largura"""
        fila = []
        fila.append(pos)
        visitados = [False for x in range(len(self.matriz))]
        visitados[pos] = True
        ordem = []
        while len(fila) > 0:
            pos = fila.pop(0)
            ordem.append(pos)
            for i,peso in self.matriz[pos]:
                if visitados[i] == False:
                    visitados[i] = True
                    fila.append(i)
        return ordem

    def colorir(self):
        """Coloracao do grafo"""
        print 'colorir!!!'
        ordenados = sorted(zip(range(len(self.matriz)),
                    map(len,self.matriz)), key=lambda k:k[1])
        ordenados.reverse()
        coloridos = [0 for x in range(len(self.matriz))]
        proxima_cor = 1
        cores = set()
        print ordenados
        for indice, grau in ordenados:
            print 'analisando indice', indice
            if coloridos[indice] != 0:
                continue
            cores_vizinhos = set()
            for vertice, peso in self.matriz[indice]:
                print 'analisando vertice', vertice
                if coloridos[vertice] != 0:
                    cores_vizinhos.add(coloridos[vertice])
            diff = cores - cores_vizinhos
            if len(diff) == 0:
                cores.add(proxima_cor)
                coloridos[indice] = proxima_cor
                proxima_cor += 1
            else:
                coloridos[indice] = diff.pop()
            print coloridos
        return coloridos

    def agmPrim(self):
        """Implentacao do algoritmo de Prim"""
        print 'prim!!!!'
        arestas = []
        agm = []
        agmVertices = [] #auxiliar
        for inicio, linha in enumerate(self.matriz):
            for fim,peso in linha:
                arestas.append((inicio, fim, peso))
        arestas = sorted(arestas, key=lambda aresta:aresta[2])
        agmVertices.append(arestas[0][0])
        agmVertices.append(arestas[0][1])
        agm.append(arestas.pop(0)[:2])

        for i in range(len(self.matriz)-1):
            for a, b, peso in arestas:
                aux = 0
                if a in agmVertices:
                    aux += 1
                if b in agmVertices:
                    aux += 2
                if (aux == 0) or (aux == 3):
                    continue
                if aux == 1:
                    agmVertices.append(b)
                else:
                    agmVertices.append(a)

                agm.append((a,b))
                arestas.remove((a,b,peso))
                break
        return agm

    def agmKruskal(self):
        """Impletancao do algoritmo de Kruskal"""
        print "Kruskal legal"[::-1]
        arestas = []
        for inicio, linha in enumerate(self.matriz):
            for fim,peso in linha:
                arestas.append((inicio, fim, peso))
        arestas = sorted(arestas, key=lambda aresta:aresta[2]) #ordena as arestas segundo seu peso
        raizes = range(len(self.matriz))
        agm = []
        print arestas
        for u,v,p in arestas:
            print raizes
            if raizes[u] != raizes[v]: #find no pseudocodigo
                agm.append((u,v))
                raiz = raizes[v]
                for i in range(len(raizes)): #uniao no pseudocodigo
                    if raizes[i] == raiz:
                        raizes[i] = raizes[u]
        print agm
        return agm

    def minDijkstra(self,source,destination):
        """Implentacao do algoritmo de Dijkstra"""
        print "Dijkstra"
        distHeap = HeapMin()
        distHeap.inserir(DijkstraNode(cfg.HIGH_VALUE, source))

        dist = [cfg.HIGH_VALUE for x in range(len(self.matriz))] #vetor para acessar de modo direto as distancias
        dist[source] = 0

        pred = [-1 for x in range(len(self.matriz))] # lista dos predecessores de cada vertice
        marcados = [-1  for x in range(len(self.matriz))]
        # inicio do algoritmo
        while len(distHeap) > 0:
            p,u = distHeap.remover()
            for v,p in self.matriz[u]:
                if dist[v] > dist[u] + p:
                    dist[v] = dist[u] + p
                    if marcados[v] == -1:
                        distHeap.inserir(DijkstraNode(dist[v], v))
                        marcados[v] = 1
                    pred[v] = u
        # usando heap in ficou O(n logn), se quiser pode melhorar usando o heap-fibonaci :)
        for i in range(len(self.matriz)):
            print i, ' ', dist[i], ' ', pred[i]
        ant = pred[destination]
        ordem = []
        #constrói o menor caminho de source para destination
        while ant != -1:
            ordem.append((ant,destination))
            destination = ant
            ant = pred[destination]
        ordem.reverse()
        return ordem

    def minBellman(self, source, dest):
        """Implementacao do algoritmo de Bellman-Ford"""
        vertices = []
        caminho = []
        for i, v in enumerate(self.matriz):
            if i != source:
                vertices.append((cfg.HIGH_VALUE, None))
            else:
                vertices.append((0, None))

        arestas = []
        for inicio, linha in enumerate(self.matriz):
            for fim,peso in linha:
                arestas.append((inicio, fim, peso))

        for i in range(len(vertices)):
            for aresta in arestas:
                ini, fim, peso = aresta
                if vertices[fim][0] > vertices[ini][0] + peso:
                    vertices[fim] = (vertices[ini][0] + peso, ini)

        #verifica ciclo negativo
        for aresta in arestas:
            ini, fim, peso = aresta
            if vertices[fim][0] > vertices[ini][0] + peso:
                print 'foo!!!'

        while source != dest:
            caminho.append((vertices[dest][1], dest))
            dest = vertices[dest][1]

        return caminho
