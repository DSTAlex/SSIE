from abc import ABC
from abc import abstractmethod

class Expression(ABC):
    @abstractmethod
    def abstractEvaluation(self, visiteur):
        pass

class BoolExpression(Expression):
    def postAssert(self, visiteur):
        return visiteur.visitPostAssert(self)

class EqTest(BoolExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitEq(self)

class InfTest(BoolExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitInf(self)
        
class NegExpression(BoolExpression):
    def __init__(self, bExp):
        self.bExp = bExp
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitNeg(self)

class IntExpression(Expression):
    def __init__(self, integer: int):
        self.integer = integer

    def abstractEvaluation(self, visiteur):
        return visiteur.visitCst(self)

class CstExp(IntExpression):
    def __init__(self, i):
        self.integer = i
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitCst(self)

class SumExp(IntExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitSum(self)

class ProdExp(IntExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitProd(self)

class DivExp(IntExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitDiv(self)

class DiffExp(IntExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitDiff(self)
	
