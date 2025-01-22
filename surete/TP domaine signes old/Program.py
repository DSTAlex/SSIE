from abc import ABC
from abc import abstractmethod

class Program:
    def __init__(self, instructions = []):
        self.instructions = instructions

class Instruction(ABC):
    pass

class Affectation(Instruction):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression.accept(self)
        
    def accept(self, visitor):
        visitor.visitAffectation(self)
        
class IfThenElse(Instruction):
    def __init__(self, bExp, thenProgram : Program, elseProgram: Program):
        self.bExp = bExp
        self.thenProgram = thenProgram
        self.elseProgram = elseProgram
        
    def accept(self, visitor):
        visitor.visitIfThenElse(self)
        
class While(Instruction):
    def __init__(self, bExp, doProgram: Program):
        self.bExp = bExp
        self.doProgram = doProgram
        
    def accept(self, visitor):
        visitor.visitWhile(self)
	
