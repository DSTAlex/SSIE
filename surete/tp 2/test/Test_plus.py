
from Interval import *

do = PlusExp(CstExp(5), CstExp(2))
vis = VisiteurInterval({})
assert(do.abstractEvaluation(vis) == (7,7))

do = PlusExp(VarExp('x'), CstExp(2))
vis = VisiteurInterval({'x':(1,5)})
assert(do.abstractEvaluation(vis) == (3,7))

do = PlusExp(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(-3, -2)})
assert(do.abstractEvaluation(vis) == (-2,3))


print("test plus ok")