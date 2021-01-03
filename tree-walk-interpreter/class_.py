from callable_ import Callable_
from instance import Instance


class Class_(Callable_):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def __str__(self):
        return self.name

    def call(self, interpreter, arugments):
        ins = Instance(self)
        initializer = self.findMethod("init")
        if initializer != None:
            initializer.bind(ins).call(interpreter,arugments)
        return ins

    def arity(self):
        initializer = self.findMethod("init")
        if initializer == None:
            return 0
        return initializer.arity()

    def findMethod(self, name):
        return self.methods.get(name)
