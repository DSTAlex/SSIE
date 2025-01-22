from Expression import * 
from Program import * 
from Domain import * 
from Visiteur import * 

class DomainSign(Domain):
    def __init__(self, dom):
        self.domain = dom.copy()
        
    def upperBound(self, s2):
        for key in self.domain:
            self.domain[key].union(s2.domain[key])
        return self.domain

class VisiteurSigne(Visiteur):
    def __init__(self, dom):
        self.dom = dom.cpy()
        
    def visitAffectation(self, affectation):
        self.dom[affectation.variable] = Expression.abstractEvaluation(self)
        
    def visitIfThenElse(self, ite: IfThenElse):
        bExp = Expression.abstractEvaluation(ite.bExp)

        execif = self.copy()
        execelse = self.copy()
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

        
    def visitWhile(self, whil: While):
        while(True in Expression.abstractEvaluation(whil.bExp)):
            for instruc in whil.doProgram:
                instruc.accept(self)
        
    def visitCst(self, cst):
        if cst.integer == 0:
            return '0'
        elif cst.integer < 0:
            return '-'
        else:
            return '+'
        
    def visitPlus(self, plus: SumExp):
        left = Expression.abstractEvaluation(plus.left)
        right = Expression.abstractEvaluation(plus.right)

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
        
    def visitDiff(self, diff: DiffExp):
        left = Expression.abstractEvaluation(diff.left)
        right = Expression.abstractEvaluation(diff.right)

        res = set()
        if '0' in left:
            for r in right:
                res.add(r)
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
        left = Expression.abstractEvaluation(prod.left)
        right = Expression.abstractEvaluation(prod.right)

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
    
    def visitDiv(self, div : DivExp):
        left = Expression.abstractEvaluation(div.left)
        right = Expression.abstractEvaluation(div.right)

        res = set()
        if '0' in left:
            res.add('0')
        if '+' in left:
            res.add('0')
            if '+' in right:
                res.add('+')
            if '-' in right:
                res.add('-')
        if '-' in left:
            res.add('0')
            if '-' in right:
                res.add('+')
            if '+' in right:
                res.add('-')
        return res
    
    def visitEq(self, eq : EqTest):
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
        
    def visitInf(self, inf : InfTest):
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

    def visitNeg(self, neg: NegExpression):
        bExp = Expression.abstractEvaluation(neg.bExp)
        res = set()
        if True in bExp:
            res.add(False)
        if False in bExp:
            res.add(True)
        return res
    
    def visitPostAssert(self, bExp):
        visiteurTest = VisiteurSigne(self.dom)
        for x in self.dom:
            psigns = set()
            for sign in self.dom[x]:
                visiteurTest.dom[x] = {sign}
                if True in bExp.abstractEvaluation(visiteurTest):
                    psigns.add(sign)
                    visiteurTest.dom[x]=psigns
        return visiteurTest.dom
