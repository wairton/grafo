#-*-coding:utf-8-*-
import math

class Reta():
    """
    Representa um segmento de reta que chamamos de reta \o/.
    y = mx + n
    """
    def __init__(self, coord):
        """'coord' representa dois pontos utilizados na definição da reta."""
        self.xa, self.ya, self.xb, self.yb = coord

    def coeAngular(self):
        """Retorna o coeficiente angular da reta."""
        if(self.xa == self.xb):
            return 10E-8
        m = float(self.yb - self.ya) / float(self.xb - self.xa)
        return m

    def coeLinear(self):
        """Retorna o coeficiente linear da reta."""
        n = (self.ya - self.coeAngular() * self.xa)
        return n

    def _checaPonto(self,coord):
        """Checa se um ponto esta contido na reta"""
        x,y = coord
        m = self.coeAngular()
        n = self.coeLinear()
        value = m*x + n
        print "value",value,"y",y
        if math.fabs(y - value) <= 3 + 10E-3:
            return True
        return False

    def checaInter(self,retaB):
        """Checa se há cruzamento entre os dois segmentos de reta. 'self' e 'retaB'"""

        ma = self.coeAngular()
        mb = retaB.coeAngular()
        na = self.coeLinear()
        nb = retaB.coeLinear()

        #checa se exite cruzamento entra as duas retas
        if math.fabs(ma - mb) <= 10E-9:
            return False

        #calcula o ponto em comun
        if retaB.xa == retaB.xb:
            xc = retaB.xa
        else:
            xc = - (float(na - nb) / float (ma - mb))
        yc = na + ma*xc

        #checa se o ponto esta no segmento
        if (self.xa - xc)*(xc - self.xb) >= 0 and (retaB.xa- xc) * (xc - retaB.xb) >= 0:
            if (self.ya - yc)*(yc - self.yb) >= 0 and (retaB.ya- yc) *(yc - retaB.yb) >= 0:
                return True
        return False
