from Expression import *
from Program import *
from Domain import *
from Visiteur import *

class DomainSign(Domain):
    def __init__(self, dom):
        self.domain = dom.copy()
        
    def upperBound(self, s2):
        for key in self.domain:
            if key in s2:
                self.domain[key] = self.domain[key].union(s2[key])
        return self.domain

class VisiteurSigne(VisiteurNonRel):
    def __init__(self, dom):
        self.dom = dom.copy()
        
    def sameVisiteur(self, domain):
        return VisiteurSigne(domain)
        
    def upperBound(self, d1, d2):
        for key in d1:
            if key in d2:
                d1[key] = d1[key].union(d2[key])
        return d1
        
    def visitVar(self, var):
        return self.dom[var.variable]
        
    def visitCst(self, cst):
        if cst.integer == 0:
            return {'0'}
        elif cst.integer < 0:
            return {'-'}
        else:
            return {'+'}

    def visitPlus(self, plus):
        leftAbstractEvaluation = plus.left.abstractEvaluation(self)
        rightAbstractEvaluation = plus.right.abstractEvaluation(self)
        if ('-' in leftAbstractEvaluation and '+' in rightAbstractEvaluation):
            return {'-','0','+'}
        if ('+' in leftAbstractEvaluation and '-' in rightAbstractEvaluation):
            return {'-','0','+'}
        res = set()
        if ('-' in leftAbstractEvaluation or '-' in rightAbstractEvaluation):
            res.add('-')
        if ('+' in leftAbstractEvaluation or '+' in rightAbstractEvaluation):
            res.add('+')
        if ('0' in leftAbstractEvaluation):
            res.union(rightAbstractEvaluation)
        if ('0' in rightAbstractEvaluation):
            res.union(leftAbstractEvaluation)
        return res

    def visitDiff(self, diff):
        leftAbstractEvaluation = diff.left.abstractEvaluation(self)
        rightAbstractEvaluation = diff.right.abstractEvaluation(self)
        if ('-' in leftAbstractEvaluation and '-' in rightAbstractEvaluation):
            return {'-','0','+'}
        if ('+' in leftAbstractEvaluation and '+' in rightAbstractEvaluation):
            return {'-','0','+'}
        res = set()
        if ('-' in leftAbstractEvaluation or '+' in rightAbstractEvaluation):
            res.add('-')
        if ('+' in leftAbstractEvaluation or '-' in rightAbstractEvaluation):
            res.add('+')
        if ('0' in leftAbstractEvaluation):
            res.union(rightAbstractEvaluation)
        if ('0' in rightAbstractEvaluation):
            res.union(leftAbstractEvaluation)
        return res
                
    def visitProd(self, prod):
        leftAbstractEvaluation = prod.left.abstractEvaluation(self)
        rightAbstractEvaluation = prod.right.abstractEvaluation(self)
        res = set()
        for leftElm in leftAbstractEvaluation:
            for rightElm in rightAbstractEvaluation:
                if ('0' == leftElm or '0' == rightElm):
                    res.add('0')
                elif (rightElm == leftElm):
                    res.add('+')
                else:
                    res.add('-')

    def visitDiv(self, div):
        leftAbstractEvaluation = div.left.abstractEvaluation(self)
        rightAbstractEvaluation = div.right.abstractEvaluation(self)
        res = set()
        for leftElm in leftAbstractEvaluation:
            for rightElm in rightAbstractEvaluation:
                if (rightElm == '0'):
                    print("Possible division par 0")
                if (leftElm == '0'):
                    res.add('0')
                elif (rightElm == leftElm):
                    res.add('+')
                else:
                    res.add('-')
        return res

    def visitEq(self, eq):
        leftAbstractEvaluation = eq.left.abstractEvaluation(self)
        rightAbstractEvaluation = eq.right.abstractEvaluation(self)
        res = set()
        for leftElm in leftAbstractEvaluation:
            for rightElm in rightAbstractEvaluation:
                if (leftElm != '0' or rightElm != '0'):
                    res.add(False)
                if (leftElm == rightElm):
                    res.add(True)
        return res

    def visitInf(self, inf):
        leftAbstractEvaluation = inf.left.abstractEvaluation(self)
        rightAbstractEvaluation = inf.right.abstractEvaluation(self)        
        res = set()
        for leftElm in leftAbstractEvaluation:
            for rightElm in rightAbstractEvaluation:
                if (leftElm == rightElm):
                        res.add(False)
                        res.add(leftElm == '0')
                elif (leftElm == '-'):
                    res.add(True)
                else:
                    res.add(rightElm == '+')
        return res

    def visitNeg(self, neg):
        abstractEvaluation = neg.bExp.abstractEvaluation(self)
        res = set()
        for elm in abstractEvaluation:
            res.add(not elm)
        return res

    def visitPostAssertEq(self, bExp):
        visiteurTest = VisiteurSigne(self.dom)
        for x in self.dom:
            psigns = set()
            for sign in self.dom[x]:
                visiteurTest.dom[x] = {sign}
                if True in bExp.abstractEvaluation(visiteurTest):
                    psigns.add(sign)
            visiteurTest.dom[x] = psigns
        return visiteurTest.dom


    def visitPostAssertInf(self, bExp):
        visiteurTest = VisiteurSigne(self.dom)
        for x in self.dom:
            psigns = set()
            for sign in self.dom[x]:
                visiteurTest.dom[x] = {sign}
                if True in bExp.abstractEvaluation(visiteurTest):
                    psigns.add(sign)
            visiteurTest.dom[x] = psigns
        return visiteurTest.dom


    def visitPostAssertNeg(self, bExp):
        visiteurTest = VisiteurSigne(self.dom)
        for x in self.dom:
            psigns = set()
            for sign in self.dom[x]:
                visiteurTest.dom[x] = {sign}
                if True in bExp.abstractEvaluation(visiteurTest):
                    psigns.add(sign)
            visiteurTest.dom[x] = psigns
        return visiteurTest.dom
