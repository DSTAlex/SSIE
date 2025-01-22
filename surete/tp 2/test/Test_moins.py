from Interval import *

do = DiffExp(CstExp(5), CstExp(2))
vis = VisiteurInterval({})
assert(do.abstractEvaluation(vis) == (3,3))

do = DiffExp(VarExp('x'), CstExp(2))
vis = VisiteurInterval({'x':(1,5)})
assert(do.abstractEvaluation(vis) == (-1,3))

do = DiffExp(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(-3, -2)})
assert(do.abstractEvaluation(vis) == (3,8))

print("test moins ok")