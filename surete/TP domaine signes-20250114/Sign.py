from Expression import *
from Program import *
from Domain import *
from Visiteur import *

class DomainSign(Domain):
    def __init__(self, dom):
        self.domain = dom.copy()
        
    def upperBound(self, s2):
        for key in self.domain:
            if key in s2.domain:
                self.domain[key] = self.domain[key].union(s2.domain[key])
        return self.domain
        
    def copy(self):
        return DomainSign(self.domain)
        
    def equals(self, d2):
        return self.domain == d2.domain

class VisiteurSigne(Visiteur):
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

    def visitPlus(self, plus: PlusExp):
        left = plus.left.abstractEvaluation(self)
        right = plus.right.abstractEvaluation(self)

        res = set()
        if '0' in left:
            for r in right:
                res.add(r)
        if '-' in left:
            if '0' in right:
                res.add('-')
            if '+' in right:
                res.add('+')
                res.add('-')
                res.add('0')
            if '-' in right:
                res.add('-')
        if '+' in left:
            if '0' in right:
                res.add('+')
            if '+' in right:
                res.add('+')
            if '-' in right:
                res.add('-')
                res.add('+')
                res.add('0')
        return res

    def visitDiff(self, diff : DiffExp):
        left = diff.left.abstractEvaluation(self)
        right = diff.right.abstractEvaluation(self)

        res = set()
        if '0' in left:
            if '0' in right:
                res.add('0')
            if '+' in right:
                res.add('-')
            if '-' in right:
                res.add('+')
        if '-' in left:
            if '0' in right:
                res.add('-')
            if '-' in right:
                res.add('+')
                res.add('-')
                res.add('0')
            if '+' in right:
                res.add('-')
        if '+' in left:
            if '0' in right:
                res.add('+')
            if '-' in right:
                res.add('+')
            if '+' in right:
                res.add('-')
                res.add('+')
                res.add('0')
        return res
                
    def visitProd(self, prod: ProdExp):
        left = prod.left.abstractEvaluation(self)
        right = prod.right.abstractEvaluation(self)

        res = set()
        if '0' in left or '0' in right:
            res.add('0')
        if '+' in left:
            for r in right:
                res.add(r)
        if '-' in left:
            if '-' in right:
                res.add('+')
            if '+' in right:
                res.add('-')
        return res

    def visitDiv(self, div: DivExp):
        left = div.left.abstractEvaluation(self)
        right = div.right.abstractEvaluation(self)

        res = set()
        if '0' in left:
            if '+' in right or '-' in right:
                res.add('0')
        if '+' in left:
            if '+' in right:
                res.add('0')
                res.add('+')
            if '-' in right:
                res.add('0')
                res.add('-')
        if '-' in left:
            if '-' in right:
                res.add('0')
                res.add('+')
            if '+' in right:
                res.add('0')
                res.add('-')
        return res

    def visitEq(self, eq):
        left = Expression.abstractEvaluation(eq.left)
        right = Expression.abstractEvaluation(eq.right)

        res = set()
        if '0' in left and '0' in right:
            res.add(True)
        for l in left:
            for r in right:
                if r == l and r != '0':
                    res.add(True)
                    res.add(False)
                else:
                    res.add(False)
        return res
        

    def visitInf(self, inf):
        left = Expression.abstractEvaluation(inf.left)
        right = Expression.abstractEvaluation(inf.right)

        res = set()
        if '+' in left:
            return {True, False}
        if '0' in left:
            if '+' in right:
                res.add(True)
            else:
                res.add(False)
        if '-' in left:
            if '-' in right:
                res.add(False)
            else:
                res.add(True)
        return res

    def visitNeg(self, neg):
        bExp = Expression.abstractEvaluation(neg.bExp)
        res = set()
        if True in bExp:
            res.add(False)
        if False in bExp:
            res.add(True)
        return res
        
    def visitAffectation(self, affectation):
        self.dom[affectation.variable] = affectation.expression.abstractEvaluation(self)
        return self.dom
        
    def visitIfThenElse(self, ite):
        bExp = Expression.abstractEvaluation(ite.bExp)

        execif = self.sameVisiteur(self.dom)
        execelse = self.sameVisiteur(self.dom)
        if True in bExp:
            execif.VisitPostAssert(ite.bExp)
            for instruc in ite.thenProgram:
                instruc.accept(execif)
        else:
            execif.dom = {}
        if False in bExp:
            execelse.VisitPostAssert(NegExpression(ite.bExp))
            for instruc in ite.elseProgram:
                instruc.accept(execelse)
        else:
            execelse.dom = {}
        
        self.dom = {}
        for key, value in execif.dom:
            self.dom[key] = value.union(execelse.dom[key])
        for key, value in execelse.dom:
            self.dom[key] = value.union(execif.dom[key])


    def visitWhile(self, whil):
        while(True in Expression.abstractEvaluation(whil.bExp)):
            for instruc in whil.doProgram:
                instruc.accept(self)

    def visitPostAssertEq(self, bExp):
        visiteurTest = VisiteurSigne(self.dom)
        for x in self.dom.domain:
            psigns = set()
            for sign in self.dom.domain[x]:
                visiteurTest.dom.domain[x] = {sign}
                if True in bExp.abstractEvaluation(visiteurTest):
                    psigns.add(sign)
            visiteurTest.dom.domain[x] = psigns
        return visiteurTest.dom


    def visitPostAssertInf(self, bExp):
        visiteurTest = VisiteurSigne(self.dom)
        for x in self.dom.domain:
            psigns = set()
            for sign in self.dom.domain[x]:
                visiteurTest.dom.domain[x] = {sign}
                if True in bExp.abstractEvaluation(visiteurTest):
                    psigns.add(sign)
            visiteurTest.dom.domain[x] = psigns
        return visiteurTest.dom


    def visitPostAssertNeg(self, bExp):
        visiteurTest = VisiteurSigne(self.dom)
        for x in self.dom.domain:
            psigns = set()
            for sign in self.dom.domain[x]:
                visiteurTest.dom.domain[x] = {sign}
                if True in bExp.abstractEvaluation(visiteurTest):
                    psigns.add(sign)
            visiteurTest.dom.domain[x] = psigns
        return visiteurTest.dom
