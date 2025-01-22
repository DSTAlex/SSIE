from Sign import *
from Interval import *
from SLevel import *

#Test de if then else pour intervalles, doit renvoyer (0,2)
the = Affectation("x", DiffExp(CstExp(0),VarExp("x")))
ite = IfThenElse(InfTest(VarExp("x"),CstExp(0)),the,Program([]))
vis = VisiteurInterval({"x":(-2,2)}, NoWidener())
print(Program([ite]).accept(vis))

#Test de while pour intervalles dans widener, doit renvoyer (0,0)
do = Affectation("x", DiffExp(VarExp("x"),CstExp(1)))
whil = While(InfTest(CstExp(0),VarExp("x")),do)
vis = VisiteurInterval({"x":(0,12)}, NoWidener())
print(Program([whil]).accept(vis))

#Test de widening vers infini, doit renvoyer (0,0)
do = Affectation("x", DiffExp(VarExp("x"),CstExp(1)))
whil = While(InfTest(CstExp(0),VarExp("x")),do)
vis = VisiteurInterval({"x":(0,12)}, InfiniteWidener())
print(Program([whil]).accept(vis))

#Test de widening vers infini, doit renvoyer (-inf,0)
do = Affectation("x", DiffExp(VarExp("x"),CstExp(1)))
whil = While(InfTest(CstExp(0),VarExp("x")),do)
vis = VisiteurInterval({"x":(12,12)}, InfiniteWidener())
print(Program([whil]).accept(vis))

#Test de widening avec seuil, doit renvoyer (-inf,0)
do = Affectation("x", DiffExp(VarExp("x"),CstExp(1)))
whil = While(InfTest(CstExp(0),VarExp("x")),do)
vis = VisiteurInterval({"x":(12,12)}, BoundedWidener(6,15))
print(Program([whil]).accept(vis))

#Test de widening avec seuil, doit renvoyer (0,0)
do = Affectation("x", DiffExp(VarExp("x"),CstExp(1)))
whil = While(InfTest(CstExp(0),VarExp("x")),do)
vis = VisiteurInterval({"x":(12,12)}, BoundedWidener(-1,15))
print(Program([whil]).accept(vis))
