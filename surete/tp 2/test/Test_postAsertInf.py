from Interval import *

do1 = InfTest(VarExp('x'), CstExp(4))

vis = VisiteurInterval({'x':(1,5)})
assert(vis.visitPostAssertInf(do1) == {"x": (1,3)})

print("test postasertinf ok")