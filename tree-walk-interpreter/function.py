from callable_ import Callable_
from environment import Environment
from return_ import Return

class Function(Callable_):
    def __init__(self,declaration,closure):
        self.declaration = declaration
        self.closure = closure

    def call(self,interpreter,arguments):
        # environment = Environment(interpreter.globals)
        environment = Environment(self.closure)
        for param,argument in zip(self.declaration.params,arguments):
            environment.define(param.lexeme,argument)
        try:
            interpreter.executeBlock(self.declaration.body,environment)
        except Return as returnValue:
            return returnValue.value

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"