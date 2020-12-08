import error

class Environment:
    def __init__(self,enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self,name,value):
        if type(name)==str:
            self.values[name] = value
        else:
            self.values[name.lexeme] = value 

    def get(self,name):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        if self.enclosing != None:
            return self.enclosing.get(name)
        raise error.RuntimeError_(name,"Undefined variable '" + name.lexeme + "'.")

    def assign(self,name,value):
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
        elif self.enclosing != None:
            self.enclosing.assign(name,value)
        else:
            raise error.RuntimeError_(name,"Undefined variable '" + name.lexeme + "'.")
