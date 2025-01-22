from Interval import *


do = InfTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(1, 5)})
assert(do.abstractEvaluation(vis) == {True, False})

do = InfTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(4, 4)})
assert(do.abstractEvaluation(vis) == {True, False})

do = InfTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(6, 7)})
assert(do.abstractEvaluation(vis) == {True})

do = InfTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(0, 0)})
assert(do.abstractEvaluation(vis) == {False})

print("test eq ok")