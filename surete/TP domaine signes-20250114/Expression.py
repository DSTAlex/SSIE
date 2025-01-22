from abc import ABC
from abc import abstractmethod

class Expression(ABC):
    @abstractmethod
    def abstractEvaluation(self, visiteur):
        pass

class BoolExpression(Expression):
    @abstractmethod
    def postAssert(self, visiteur):
        pass

class EqTest(BoolExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitEq(self)

    def postAssert(self, visiteur):
        return visiteur.visitPostAssertEq(self)

class InfTest(BoolExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitInf(self)

    def postAssert(self, visiteur):
        return visiteur.visitPostAssertInf(self)
        
class NegExpression(BoolExpression):
    def __init__(self, bExp):
        self.bExp = bExp
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitNeg(self)

    def postAssert(self, visiteur):
        return visiteur.visitPostAssertNeg(self)

class IntExpression(Expression):
    def __init__(self, integer: int):
        self.integer = integer

    def abstractEvaluation(self, visiteur):
        return visiteur.visitCst(self)

class VarExp(IntExpression):
    def __init__(self, v):
        self.variable = v
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitVar(self)

    def postAssert(self, visiteur, dom):
        return visiteur.visitPostAssertVar(self, dom)

class CstExp(IntExpression):
    def __init__(self, i):
        self.integer = i
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitCst(self)

    def postAssert(self, visiteur, dom):
        return visiteur.visitPostAssertCst(self, dom)

class PlusExp(IntExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def abstractEvaluation(self, visiteur):
        return visiteur.visitPlus(self)

    def postAssert(self, visiteur, dom):
        return visiteur.visitPostAssertPlus(self, dom)

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

    def postAssert(self, visiteur, dom):
        return visiteur.visitPostAssertDiff(self, dom)
	
