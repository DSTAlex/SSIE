from abc import abstractmethod
from Expression import *
from Program import *
from Domain import *

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
        
class VisiteurNonRel(Visiteur):
    def __init__(self):
        pass
        
    def visitAffectation(self, affectation):
        self.dom[affectation.variable] = affectation.expression.abstractEvaluation(self)
        return self.dom
        
    def visitIfThenElse(self, ite):
        expression = ite.bExp
        notexpression = NegExpression(expression)
        visiteurThen = self.sameVisiteur(expression.postAssert(self))
        visiteurElse = self.sameVisiteur(notexpression.postAssert(self))
        domThen = ite.thenProgram.accept(visiteurThen)
        domElse = ite.elseProgram.accept(visiteurElse)
        self.dom = self.upperBound(domThen,domElse)
        return self.dom

    def visitWhile(self, whil):
        whilExp = whil.bExp
        notExp = NegExpression(whilExp)
        whilDom = self.dom
        whilDom1 = whil.doProgram.accept(self.sameVisiteur(whilExp.postAssert(self)))
        self.upperBound(whilDom1,whilDom)
        while (not (whilDom1 == whilDom)):
            whilDom = whilDom1
            whilDom1 = whil.doProgram.accept(self.sameVisiteur(whilExp.postAssert(self)))
            self.upperBound(whilDom1, whilDom)
        self.dom = whilDom
        self.dom = notExp.postAssert(self)
        return self.dom
        
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
