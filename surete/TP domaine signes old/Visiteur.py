from abc import abstractmethod

class Visiteur:
    def __init__(self):
        pass
        
    @abstractmethod
    def visitAffectation(self, affectation):
        pass
        
    @abstractmethod
    def visitIfThenElse(self, ite):
        pass
        
    @abstractmethod
    def visitWhile(self, whil):
        pass
        
    @abstractmethod
    def visitPlus(self, plus):
        pass
        
    @abstractmethod
    def visitDiff(self, diff):
        pass
        
    @abstractmethod
    def visitProd(self, prod):
        pass
        
    @abstractmethod
    def visitDiv(self, div):
        pass
        
    @abstractmethod
    def visitEq(self, eq):
        pass
        
    @abstractmethod
    def visitInf(self, inf):
        pass
