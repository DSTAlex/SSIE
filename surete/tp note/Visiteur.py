from abc import abstractmethod
from Expression import *
from Program import *
from Domain import *
from Widener import *


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
        #TODO modifier visitWhile pour permettre le déroulement de boucle
        #Le nombre de déroulements à effectuer est donné par self.ulevel
        whilExp = whil.bExp
        notExp = NegExpression(whilExp)
        whilDom = self.dom.copy()
        whilDom1 = whil.doProgram.accept(self.sameVisiteur(whilExp.postAssert(self.sameVisiteur(whilDom))))
        self.upperBound(whilDom1,whilDom)
        i = 0
        while (not (whilDom1 == whilDom)):
            self.dom = whilDom1.copy()
            whilDom = whilDom1.copy()
            whilDom1 = whil.doProgram.accept(self.sameVisiteur(whilExp.postAssert(self.sameVisiteur(whilDom))))
            if i >= self.ulevel:
                whilDom1 = self.widener.widening(whilDom, whilDom1) 
            i += 1
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
