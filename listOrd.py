#-*-coding:utf-8 -*-
class ListOrd(list):
	"""
	Lista capaz de inserir elementos de modo ordenado.
	Cada elemento é uma tupla (índice, peso)
	"""
	def add(self, indice, peso=-1):
		"""adiciona elementos à lista ordenados por (indice)"""
		for i in range(len(self)):
			if indice < self[i][0]:
				self.insert(i,(indice, peso))
				break
			elif indice == self[i][0]:
				break
		else:
			self.append((indice, peso))
			
	def reduzir(self, indice):
		"""Reduz os valores da lista"""
		posicao, tamanho = 0, len(self)
		while posicao < tamanho:
			if indice == self[posicao][0]:
				del self[indice]
				tamanho -= 1
			elif indice < self[posicao][0]:
				self[posicao] = (self[posicao][0]-1, self[posicao][1])
			posicao += 1

				
	def remover(self, indice):
		"""remove o elemento indicado por (indice) da lista"""
		for n, peso in self:
			if indice == n:
				self.remove((n,peso))
	
	def indice(self, indice):
		"""Retorna a posicao do elemento indice na lista"""
		for n in xrange(len(self)):
			if indice == self[n][0]:
				return n
		return None
	
	
	def peso(self, indice):	
		"""Retorna o peso do vertice indice"""
		for n in xrange(len(self)):
			if indice == self[n][0]:
				return self[n][1]
		return None
		
		
		
	def _print(self):
		"""imprimi a lista no terminal"""
		for x in range(len(self)):
			print self[x],
