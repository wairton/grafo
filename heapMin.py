#-*-coding:utf-8-*-
import math

class HeapMin:
	"""
	Fila de prioriades usando Heap Mínimo.
	Cada elemento é uma tupla (índice, peso).	
	"""
	def __init__(self):
		self.L = []
		
	def _minHeapify(self,i):
		"""posiciona o elemento i no Heap. Método recursivo."""
		l = 2*i + 1;
		r = 2*i + 2;
		minV = i
		if l < len(self.L) and self.L[l][1] < self.L[i][1]:
			minV = l;
		if r < len(self.L) and self.L[r][1] < self.L[minV][1]:
			minV = r;
		if  minV != i: 
			self.L[i],self.L[minV] = self.L[minV],self.L[i]
			self._minHeapify(minV);
			
	def _buildMin(self):
		"""Monta o Heap Mínimo utilizando o método _minHeapify"""
		i = len(self.L);
		for i in range(i/2 -1,-1,-1):
			self._minHeapify(i);

	def _subir(self,i):
		"""Corrige o topo do Heap após uma inserção."""
		j = (int) (math.ceil(i/2)) - 1
		if i > 0:
			if self.L[j][1] > self.L[i][1]:
				self.L[i],self.L[j] = self.L[j],self.L[i]
				self.subir(j)
				
	def inserir(self,chave):
		"""Insere um elemento no Heap."""
		self.L.append(chave)
		self._subir(len(self.L)-1)
		
	def remover(self):
		"""Remove um elemento do Heap."""	
		minV = self.L[0]
		self.L[0] = self.L[-1]
		self.L[-1] = minV
		self.L.pop()
		self._minHeapify(0)
		return minV	
		
	def heapLen(self):
		"""Retorna o tamanho do Heap."""	
		return len(self.L)	
