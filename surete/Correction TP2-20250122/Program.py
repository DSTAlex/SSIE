from abc import ABC
from abc import abstractmethod

class Program:
    def __init__(self, instructions = []):
        self.instructions = instructions
    def accept(self, visitor):
        for elm in self.instructions:
            visitor.dom = elm.accept(visitor)
        return visitor.dom

class Instruction(ABC):
    pass

class Affectation(Instruction):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
        
    def accept(self, visitor):
        return visitor.visitAffectation(self)
        
class IfThenElse(Instruction):
    def __init__(self, bExp, thenProgram, elseProgram):
        self.bExp = bExp
        self.thenProgram = thenProgram
        self.elseProgram = elseProgram
        
    def accept(self, visitor):
        return visitor.visitIfThenElse(self)
        
class While(Instruction):
    def __init__(self, bExp, doProgram):
        self.bExp = bExp
        self.doProgram = doProgram
        
    def accept(self, visitor):
        return visitor.visitWhile(self)
	
