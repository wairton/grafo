# -*-coding:utf-8-*-
import math


class Reta(object):
    """
    Representa um segmento de reta que chamamos de reta \o/.
    y = mx + n
    """
    def __init__(self, coord):
        """'coord' representa dois pontos utilizados na definição da reta."""
        self.xa, self.ya, self.xb, self.yb = coord

    def coeficiente_angular(self):
        """Retorna o coeficiente angular da reta."""
        if(self.xa == self.xb):
            return 10E-8
        m = float(self.yb - self.ya) / float(self.xb - self.xa)
        return m

    def coeficiente_linear(self):
        """Retorna o coeficiente linear da reta."""
        n = (self.ya - self.coeficiente_angular() * self.xa)
        return n

    def checa_ponto(self, coord):
        """Checa se um ponto esta contido na reta"""
        x, y = coord
        m = self.coeficiente_angular()
        n = self.coeficiente_linear()
        value = m * x + n
        if math.fabs(y - value) <= 3 + 10E-3:
            return True
        return False

    def checaInter(self, outra_reta):
        """
        Checa se há cruzamento entre 'self' e 'outra_reta'.
        """
        ma = self.coeficiente_angular()
        mb = outra_reta.coeficiente_angular()
        na = self.coeficiente_linear()
        nb = outra_reta.coeficiente_linear()

        if math.fabs(ma - mb) <= 10E-9:
            return False
        if outra_reta.xa == outra_reta.xb:
            xc = outra_reta.xa
        else:
            xc = -(float(na - nb) / float(ma - mb))
        yc = na + ma * xc

        # checa se o ponto esta no segmento
        if (self.xa - xc)*(xc - self.xb) >= 0 and (outra_reta.xa- xc) * (xc - outra_reta.xb) >= 0:
            if (self.ya - yc)*(yc - self.yb) >= 0 and (outra_reta.ya- yc) *(yc - outra_reta.yb) >= 0:
                return True
        return False
