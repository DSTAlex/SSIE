from Sign import *
from Interval import *

import test.Test_plus
import test.Test_moins
import test.Test_eq
import test.Test_inf
import test.Test_postAsertInf

the = Affectation("x", DiffExp(CstExp(0),VarExp("x")))
ite = IfThenElse(InfTest(VarExp("x"),CstExp(0)),the,Program([]))
vis = VisiteurSigne({"x":{'+','0','-'}})
print(Program([ite]).accept(vis))

do = Affectation("x", DiffExp(VarExp("x"),CstExp(1)))
whil = While(InfTest(CstExp(0),VarExp("x")),do)
vis = VisiteurSigne({"x":{'+'}})
print(Program([whil]).accept(vis))


