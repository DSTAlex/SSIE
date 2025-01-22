from Sign import *
from Interval import *

the = Affectation("x", DiffExp(CstExp(0),VarExp("x")))
ite = IfThenElse(InfTest(VarExp("x"),CstExp(0)),the,Program([]))
vis = VisiteurInterval({"x":(-2,2)})
print(InfTest(VarExp("x"),CstExp(0)).postAssert(vis))
print(Program([ite]).accept(vis))

do = Affectation("x", DiffExp(VarExp("x"),CstExp(1)))
whil = While(InfTest(CstExp(0),VarExp("x")),do)
vis = VisiteurInterval({"x":(0,12)})
print(Program([whil]).accept(vis))
