from Interval import *

do = EqTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(-3, -2)})
assert(do.abstractEvaluation(vis) == {False})

do = EqTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(-1, 2)})
assert(do.abstractEvaluation(vis) == {True, False})

do = EqTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(-1, 1)})
assert(do.abstractEvaluation(vis) == {True, False})

do = EqTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(5, 7)})
assert(do.abstractEvaluation(vis) == {True, False})

do = EqTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(1,5), "y":(1, 5)})
assert(do.abstractEvaluation(vis) == {True, False})

do = EqTest(VarExp('x'), VarExp("y"))
vis = VisiteurInterval({'x':(-2,-2), "y":(-2, -2)})
assert(do.abstractEvaluation(vis) == {True})

print("test eq ok")