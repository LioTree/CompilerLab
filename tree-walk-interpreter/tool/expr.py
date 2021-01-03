from abc import ABCMeta, abstractmethod

class Expr(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
      pass

class This(Expr):
    def __init__(self,keyword):
        self.keyword=keyword

    def accept(self,visitor):
        return visitor.visitThisExpr(self)

class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def visitThisExpr(self,exp):
        pass

