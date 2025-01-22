from Expression import *
from Program import *
from Domain import *
from Visiteur import *

class Interval(Domain):
    def __init__(self, domain):
        self.dom = domain
        
    def upperBound(self, s2):
        for key in self.domain:
            if key in s2:
                self.domain[key] = (min(self.domain[key][0],s2[key][0]) , max(self.domain[key][1],s2[key][1]))
        return self.domain
        
    def lowerBound(self, s2):
        for key in self.domain:
            if key in s2:
                self.domain[key] = (max(self.domain[key][0],s2[key][0]) , min(self.domain[key][1],s2[key][1]))
        return self.domain

class VisiteurInterval(VisiteurNonRel):
    def __init__(self, dom):
        self.dom = dom.copy()
        
    def sameVisiteur(self, domain):
        return VisiteurInterval(domain)
        
    def upperBound(self, d1, d2):
        return d1.upperBound(d2)
        
    def visitVar(self, var):
        return self.dom[var.variable]
        
    def visitCst(self, cst):
        return (cst.integer, cst.integer)

    def visitPlus(self, plus : PlusExp):
        leftAbstractEvaluation = plus.left.abstractEvaluation(self)
        rightAbstractEvaluation = plus.right.abstractEvaluation(self)
        a,b = leftAbstractEvaluation
        c,d = rightAbstractEvaluation
        return (a+c, b+d)

    def visitDiff(self, diff : DiffExp):
        leftAbstractEvaluation = diff.left.abstractEvaluation(self)
        rightAbstractEvaluation = diff.right.abstractEvaluation(self)
        a,b = leftAbstractEvaluation
        c,d = rightAbstractEvaluation
        return (a-d, b-c)

    def visitEq(self, eq : EqTest):
        a, b = eq.left.abstractEvaluation(self)
        c, d = eq.right.abstractEvaluation(self)
        if a == b and b == c and c == d:
            return {True}
        else:
            res = {False}
            if b >= c and a <= d:
                res.add(True)
            if d >= a and c <= b:
                res.add(True)
        return res
        

    def visitInf(self, inf: InfTest):
        a, b = inf.left.abstractEvaluation(self)
        c, d = inf.right.abstractEvaluation(self)

        res = set()
        if a < d:
            res.add(True)
        if b >= c:
            res.add(False)
        return res

    def visitNeg(self, neg):
        abstractEvaluation = neg.bExp.abstractEvaluation(self)
        res = set()
        for elm in abstractEvaluation:
            res.add(not elm)
        return res

    def visitPostAssertEq(self, bExp):
        leftAbstractEvaluation = bExp.left.abstractEvaluation(self)
        rightAbstractEvaluation = bExp.right.abstractEvaluation(self)
        bExp.left.postAssert(self,rightAbstractEvaluation)
        bExp.right.postAssert(self,leftAbstractEvaluation)
        return self.dom

    def visitPostAssertInf(self, bExp : BoolExpression):
        rightAbstractEvaluation = bExp.right.abstractEvaluation(self)
        bExp.left.postAssert(self,rightAbstractEvaluation)
        return self.dom
    
    def visitPostAssertVar(self, var: VarExp):
        pass

    def visitPostAssertPlus(self, plus, domain):
        pass

    def visitPostAssertDiff(self, diff, domain):
        pass
