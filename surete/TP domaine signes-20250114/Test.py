from Expression import * 
from Program import * 
from Domain import * 
from Visiteur import * 
from Sign import *


def test_cst_plus():
    value : IntExpression = IntExpression(5)
    afectation : Affectation = Affectation('x', value)
    visitor : VisiteurSigne = VisiteurSigne({})
    afectation.accept(visitor)
    assert(visitor.dom['x'] == {'+'})
    print("cst + OK")

def test_cst_moins():
    value : IntExpression = IntExpression(-5)
    afectation : Affectation = Affectation('x', value)
    visitor : VisiteurSigne = VisiteurSigne({})
    afectation.accept(visitor)
    assert(visitor.dom['x'] == {'-'})
    print("cst - OK")

def test_cst_0():
    value : IntExpression = IntExpression(0)
    afectation : Affectation = Affectation('x', value)
    visitor : VisiteurSigne = VisiteurSigne({})
    afectation.accept(visitor)
    assert(visitor.dom['x'] == {'0'})
    print("cst 0 OK")

def test_plus1():
    value_left : IntExpression = IntExpression(5)
    value_right : IntExpression = IntExpression(5)
    plus_exp : PlusExp = PlusExp(value_left, value_right)
    affectation : Affectation = Affectation('x', plus_exp)
    visiteur : VisiteurSigne = VisiteurSigne({})
    affectation.accept(visiteur)
    assert(visiteur.dom['x'] == {'+'})
    print("{+} + {+} = {+}")

def test_plus2():
    value_left : IntExpression = IntExpression(0)
    value_right : IntExpression = IntExpression(5)
    plus_exp : PlusExp = PlusExp(value_left, value_right)
    affectation : Affectation = Affectation('x', plus_exp)
    visiteur : VisiteurSigne = VisiteurSigne({})
    affectation.accept(visiteur)
    assert(visiteur.dom['x'] == {'+'})
    print("{ 0 } + {+} = {+}")

def test_plus3():
    value_left : IntExpression = IntExpression(5)
    value_right : IntExpression = IntExpression(0)
    plus_exp : PlusExp = PlusExp(value_left, value_right)
    affectation : Affectation = Affectation('x', plus_exp)
    visiteur : VisiteurSigne = VisiteurSigne({})
    affectation.accept(visiteur)
    assert(visiteur.dom['x'] == {'+'})
    print("{+} + { 0 } = {+}")

def test_plus4():
    value_left : IntExpression = IntExpression(0)
    value_right : IntExpression = IntExpression(0)
    plus_exp : PlusExp = PlusExp(value_left, value_right)
    visiteur : VisiteurSigne = VisiteurSigne({})
    assert({'0'} == plus_exp.abstractEvaluation(visiteur))
    print("{ 0 } + { 0 } = { 0 }")

def test_plus5():
    left = {'+', '-'}
    right = {'+'}
    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    plus_exp : PlusExp = PlusExp(value_left, value_right)
    expect = {'+', '-', '0'}
    got = plus_exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "+",right," = ", expect)

def test_plus6():
    left = {'+', '0'}
    right = {'+'}
    expect = {'+'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    plus_exp : PlusExp = PlusExp(value_left, value_right)
    got = plus_exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "+",right," = ", expect)

def test_plus7():
    left = {'+', '0'}
    right = {'+', '0'}
    expect = {'+', '0'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    plus_exp : PlusExp = PlusExp(value_left, value_right)
    got = plus_exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "+",right," = ", expect)

def test_moins1():
    left = {'+'}
    right = {'+'}
    expect = {'+', '0', '-'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    moins_exp = DiffExp(value_left, value_right)
    got = moins_exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "-",right," = ", expect)

def test_moins2():
    left = {'-'}
    right = {'+'}
    expect = {'-'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    moins_exp = DiffExp(value_left, value_right)
    got = moins_exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "-",right," = ", expect)

def test_moins3():
    left = {'+'}
    right = {'0'}
    expect = {'+'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    moins_exp = DiffExp(value_left, value_right)
    got = moins_exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "-",right," = ", expect)

def test_moins4():
    left = {'-'}
    right = {'+', '0'}
    expect = {'-'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    moins_exp = DiffExp(value_left, value_right)
    got = moins_exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "-",right," = ", expect)

def test_moins5():
    left = {'-', '0'}
    right = {'+', '0'}
    expect = {'-', '0'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    moins_exp = DiffExp(value_left, value_right)
    got = moins_exp.abstractEvaluation(visiteur)
    print(got)
    assert(expect == got)
    print(left, "-",right," = ", expect)

def test_mult1():
    left = {'-'}
    right = {'-'}
    expect = {'+'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = ProdExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "*",right," = ", expect)

def test_mult2():
    left = {'+'}
    right = {'+'}
    expect = {'+'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = ProdExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "*",right," = ", expect)

def test_mult3():
    left = {'+'}
    right = {'-'}
    expect = {'-'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = ProdExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "*",right," = ", expect)

def test_mult4():
    left = {'+'}
    right = {'0'}
    expect = {'0'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = ProdExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "*",right," = ", expect)

def test_mult5():
    left = {'+', '0'}
    right = {'+'}
    expect = {'+', '0'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = ProdExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "*",right," = ", expect)

def test_mult6():
    left = {'+', '-'}
    right = {'+'}
    expect = {'+', '-'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = ProdExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "*",right," = ", expect)

def test_div1():
    left = {'+'}
    right = {'+'}
    expect = {'+', '0'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = DivExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "/",right," = ", expect)

def test_div2():
    left = {'+', '-', '0'}
    right = {'0'}
    expect = set()

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = DivExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "/",right," = ", expect)

def test_div3():
    left = {'+'}
    right = {'0', '+'}
    expect = {'+', '0'}

    visiteur : VisiteurSigne = VisiteurSigne({'x' : left, 'y' : right})
    value_left : VarExp= VarExp('x')
    value_right : IntExpression = VarExp('y')
    exp = DivExp(value_left, value_right)
    got = exp.abstractEvaluation(visiteur)
    assert(expect == got)
    print(left, "/",right," = ", expect)


def run_all():
    print("cst")
    test_cst_0()
    test_cst_moins()
    test_cst_plus()

    print('+')
    test_plus1()
    test_plus2()
    test_plus3()
    test_plus4()
    test_plus5()
    test_plus6()
    test_plus7()

    print('-')
    test_moins1()
    test_moins2()
    test_moins3()
    test_moins4()
    test_moins5()

    print('*')
    test_mult1()
    test_mult2()
    test_mult3()
    test_mult4()
    test_mult5()
    test_mult6()

    print('/')
    test_div1()
    test_div2()
    test_div3()

run_all()