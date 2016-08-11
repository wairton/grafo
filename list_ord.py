# -*-coding:utf-8 -*-


class ListOrd(list):
    """
    Lista capaz de inserir elementos de modo ordenado.
    Cada elemento � uma tupla (�ndice, peso)
    """
    def add(self, indice, peso=-1):
        """adiciona elementos � lista ordenados por (indice)"""
        for i in range(len(self)):
            if indice < self[i][0]:
                self.insert(i, (indice, peso))
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
                self[posicao] = (self[posicao][0] - 1, self[posicao][1])
            posicao += 1

    def remover(self, indice):
        """remove o elemento indicado por (indice) da lista"""
        for n, peso in self:
            if indice == n:
                self.remove((n, peso))

    def indice(self, indice):
        """Retorna a posicao do elemento indice na lista"""
        for i, item in enumerate(self):
            if item[0] == indice:
                return i
        return None

    def peso(self, indice):
        """Retorna o peso do vertice indice"""
        for item in self:
            if item[0] == indice:
                return item[1]
        return None
