# -*-coding:utf-8-*-
import math
import heapq
from collections import namedtuple


DijkstraNode = namedtuple('DijkstraNode', ['distance', 'label'])


class HeapMin(object):
    """
    Classe que encapsula funcões da lib heapq

    Cada elemento é uma tupla (peso, índice).
    """
    def __init__(self):
        self.heap = []

    def inserir(self, chave):
        """Insere um elemento no Heap."""
        heapq.heappush(self.heap, chave)

    def remover(self):
        """Remove e retorna o menor elemento do Heap."""
        return heapq.heappop(self.heap)

    def __len__(self):
        return len(self.heap)
