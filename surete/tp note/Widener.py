from abc import abstractmethod
from Expression import *
from Program import *
from Domain import *

INF = float("inf")
NEGINF = - INF

class Widener:
    def __init__(self):
        pass
        
    @abstractmethod
    def widening(self, leftDom, rightDom):
        pass
        
class NoWidener(Widener):
    def __init__(self):
        visiteur = 0
        
    def widening(self, leftDom, rightDom):
        return self.visiteur.upperBound(leftDom,rightDom)
        
class InfiniteWidener(Widener):
    def __init__(self):
        visiteur = 0
        
    #Prend en entr�e 2 intervalle et renvoi le r�sultat du widening de ces intervalles
    def wideningInterval(self, leftDom, rightDom):
        a,b = leftDom
        c,d = rightDom
        if a <= c and b >= d:
            return (a,b)
        elif c < a and b >= d:
            return (NEGINF , b)
        elif d > b and a <= c:
            return (a, INF)
        else:
            return (NEGINF, INF)
	
       
    #Prend en entr�e 2 domaines (dictionnaires)et renvoi le r�sultat du widening de ces domaines 
    def widening(self, leftDom, rightDom):
        res = {}
        for left in leftDom:
            if left in rightDom:
                res[left] = self.wideningInterval(leftDom[left], rightDom[left])
            else:
                res[left] = leftDom[left]
        
        for right in rightDom:
            if right not in leftDom:
                res[right] = rightDom[right]
        return res
    
class BoundedWidener(Widener):
    def __init__(self, lowBound, highBound):
        self.visiteur = 0
        self.lowBound = lowBound
        self.highBound = highBound
        
    #Prend en entr�e 2 intervalle et renvoi le r�sultat du widening de ces intervalles
    def wideningInterval(self, leftDom, rightDom):
        a,b = leftDom
        c,d = rightDom
        lbound = c
        hbound = d
        if c < self.lowBound:
            lbound = NEGINF
        if d > self.lowBound:
            hbound = INF

        if a <= c and b >= d:
            return (a,b)
        elif c < a and b >= d:
            return (lbound, b)
        elif d > b and a <= c:
            return (a, hbound)
        else:
            return (lbound, hbound)
        
    #Prend en entr�e 2 domaines (dictionnaires)et renvoi le r�sultat du widening de ces domaines
    def widening(self, leftDom, rightDom):
        res = {}
        for left in leftDom:
            if left in rightDom:
                res[left] = self.wideningInterval(leftDom[left], rightDom[left])
            else:
                res[left] = leftDom[left]
        
        for right in rightDom:
            if right not in leftDom:
                res[right] = rightDom[right]
        return res
