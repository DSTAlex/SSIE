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

class VisiteurSLevel:
    
    def __init__(self, visiteurs, widener, ulevel=0):
        #visiteurs est une liste de visiteur
        self.visiteurs = visiteurs
        self.widener = widener
        self.widener.visiteur = self
        self.ulevel = ulevel
    
    #on fusionne tous les états possibles en un seul
    def fusion(self):
        dom = visiteurs[0].dom.copy()
        for v in visiteurs:
            dom = upperBound(dom, v.dom)
        return visiteur[0].sameVisiteur(dom)
        
    def sameVisiteur(self, domain):
        return VisiteurInterval(domain, self.widener)
        
    def visitAffectation(self, affectation):
        for v in visiteurs:
            v.visitAffectation(affectation)
        return self.visiteurs
        
    def visitIfThenElse(self, ite: IfThenElse):
        expression : BoolExpression = ite.bExp
        notexpression = NegExpression(expression)
        visiteursThen = []
        visiteursElse = []
        #TODO        
        for v in self.visiteurs:
            then_visitor = v.copy()
            else_visitor = v.copy()
            if_possible = expression.abstractEvaluation(v)
            if True in if_possible:
                then_visitor.visitPostAssertEq(expression)
                ite.thenProgram(then_visitor)
                visiteursThen.add(then_visitor)
            if False in if_possible:
                else_visitor.visitPostAssertEq(notexpression)
                ite.elseProgram(else_visitor)
                visiteursElse.add(else_visitor)
        self.visiteurs = visiteursThen + visiteursElse
        return self.visiteurs

    def visitWhile(self, whil):
        for v in self.visiteurs:
            v = self.visitWhileForOneState(whil, v)
        return self.visiteurs

    def visitWhileForOneState(self, whil : While, visiteur):
        #TODO
        whil.accept(visiteur)
        visiteur.fusion()
        return visiteur
