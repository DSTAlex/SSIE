from Expression import *
from Program import *
from Domain import *
from Visiteur import *

def upperBoundInter(d1, d2):
    return (min(d1[0],d2[0]) , max(d1[1],d2[1]))
    
def lowerBoundInter(d1, d2):
    return (max(d1[0],d2[0]) , min(d1[1],d2[1]))
        
def upperBound(s1, s2):
    for key in s1:
        if key in s2:
            s1[key] = upperBoundInter(s1[key], s2[key])
    return s1
        
def lowerBound(s1, s2):
    for key in s1:
        if key in s2:
            s1[key] = lowerBoundInter(s1[key], s2[key])
    return s1

class VisiteurInterval(VisiteurNonRel):
    
    def __init__(self, domain, widener, ulevel=0):
        self.dom = domain.copy()
        self.widener = widener
        self.widener.visiteur = self
        self.ulevel = ulevel
    
    def copy(self):
        return VisiteurInterval(self.dom, self.widener, self.ulevel)
        
    def sameVisiteur(self, domain):
        return VisiteurInterval(domain, self.widener, self.ulevel)
        
    def upperBound(self, d1, d2):
        return upperBound(d1,d2)
        
    def visitVar(self, var):
        return self.dom[var.variable]
        
    def visitCst(self, cst):
        return (cst.integer, cst.integer)

    def visitPlus(self, plus):
        leftAbsEval = plus.left.abstractEvaluation(self)
        rightAbsEval = plus.right.abstractEvaluation(self)
        return (leftAbsEval[0]+rightAbsEval[0], leftAbsEval[1]+rightAbsEval[1])

    def visitDiff(self, diff):
        leftAbsEval = diff.left.abstractEvaluation(self)
        rightAbsEval = diff.right.abstractEvaluation(self)
        return (leftAbsEval[0]-rightAbsEval[1], leftAbsEval[1]-rightAbsEval[0])

    def visitEq(self, eq):
        leftAbstractEvaluation = eq.left.abstractEvaluation(self)
        rightAbstractEvaluation = eq.right.abstractEvaluation(self)
        res = set()
        if (leftAbstractEvaluation[0] <= rightAbstractEvaluation[1] and rightAbstractEvaluation[0] <= leftAbstractEvaluation[1]):
            res.add(True)
        if (leftAbstractEvaluation[0] != leftAbstractEvaluation[1] or rightAbstractEvaluation[0] != rightAbstractEvaluation[1] or rightAbstractEvaluation[0] != leftAbstractEvaluation[0]):
            res.add(False)
        return res

    def visitInf(self, inf):
        leftAbstractEvaluation = inf.left.abstractEvaluation(self)
        rightAbstractEvaluation = inf.right.abstractEvaluation(self)
        res = set()
        if (leftAbstractEvaluation[0] < rightAbstractEvaluation[1]):
            res.add(True)
        if (leftAbstractEvaluation[1] >= rightAbstractEvaluation[0]):
            res.add(False)
        return res

    def visitNeg(self, neg):
        abstractEvaluation = neg.bExp.abstractEvaluation(self)
        res = set()
        for elm in abstractEvaluation:
            res.add(not elm)
        return res

    def visitPostAssertCst(self, cst, domain):
        return self.dom

    def visitPostAssertVar(self, var, domain):
        self.dom[var.variable] = lowerBoundInter(self.dom[var.variable], domain)
        return self.dom

    def visitPostAssertNeg(self, neg):
        neg.bExp.postNAssert(self)
        return self.dom

    def visitPostAssertNNeg(self, neg):
        neg.bExp.postAssert(self)
        return self.dom

    def visitPostAssertEq(self, bExp):
        absEval = lowerBoundInter(bExp.left.abstractEvaluation(self),bExp.right.abstractEvaluation(self))
        bExp.left.postAssert(self,absEval)
        bExp.right.postAssert(self,absEval)
        return self.dom

    def visitPostAssertNEq(self, bExp):       
        leftAbsEval = bExp.left.abstractEvaluation(self)
        rightAbsEval = bExp.right.abstractEvaluation(self)
        if leftAbsEval[0] == leftAbsEval[1]:
            if leftAbsEval[0] == rightAbsEval[0]:
                rightAbsEval[0]+=1
            if leftAbsEval[0] == rightAbsEval[1]:
                rightAbsEval[1]-=1
        if rightAbsEval[0] == rightAbsEval[1]:
            if leftAbsEval[0] == rightAbsEval[0]:
                leftAbsEval[0]+=1
            if leftAbsEval[1] == rightAbsEval[0]:
                leftAbsEval[1]-=1
        bExp.left.postAssert(self,leftAbsEval)
        bExp.right.postAssert(self,rightAbsEval)
        return self.dom

    def visitPostAssertInf(self, bExp):     
        leftAbsEval = bExp.left.abstractEvaluation(self)
        rightAbsEval = bExp.right.abstractEvaluation(self)
        bExp.right.postAssert(self,(max(rightAbsEval[0],leftAbsEval[0]+1),rightAbsEval[1]))
        bExp.left.postAssert(self,(leftAbsEval[0], min(leftAbsEval[1],rightAbsEval[1]-1)))
        return self.dom

    def visitPostAssertNInf(self, bExp):     
        leftAbsEval = bExp.left.abstractEvaluation(self)
        rightAbsEval = bExp.right.abstractEvaluation(self)
        bExp.left.postAssert(self,(max(leftAbsEval[0],rightAbsEval[0]),leftAbsEval[1]))
        bExp.right.postAssert(self,(rightAbsEval[0], min(rightAbsEval[1],leftAbsEval[1])))
        return self.dom

    def visitPostAssertPlus(self, plus, domain):   
        leftAbsEval = plus.left.abstractEvaluation(self)
        rightAbsEval = plus.right.abstractEvaluation(self)
        leftAbsEval = lowerBoundInter(leftAbsEval, (domain[0]-rightAbsEval[1], domain[1]-rightAbsEval[0]))
        rightAbsEval = lowerBoundInter(rightAbsEval, (domain[0]-leftAbsEval[1], domain[1]-leftAbsEval[0]))
        bExp.left.postAssert(self,leftAbsEval)
        bExp.right.postAssert(self,rightAbsEval)
        return self.dom

    def visitPostAssertDiff(self, diff, domain):  
        leftAbsEval = plus.left.abstractEvaluation(self)
        rightAbsEval = plus.right.abstractEvaluation(self)
        leftAbsEval = lowerBoundInter(leftAbsEval, (domain[0]+rightAbsEval[0], domain[1]+rightAbsEval[1]))
        rightAbsEval = lowerBoundInter(rightAbsEval, (leftAbsEval[0]-domain[1], leftAbsEval[1]-domain[0]))
        bExp.left.postAssert(self,leftAbsEval)
        bExp.right.postAssert(self,rightAbsEval)
        return self.dom
