import expr
import stmt
from error import ParseError, hadError
from enum import Enum, auto


class FunctionType(Enum):
    NONE = auto(),
    FUNCTION = auto()


class Resolver(expr.Visitor, stmt.Visitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.currentFunction = FunctionType.NONE

    def visitBlockStmt(self, stmt):
        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()

    def visitVarStmt(self, statement):
        self.declare(statement.name)
        if statement.name != None:
            self.resolve(statement.initializer)
        self.define(statement.name)

    def resolve(self, args):
        try:
            if isinstance(args, list):
                statements = args
                for statement in statements:
                    self.resolve(statement)
            elif isinstance(args, stmt.Stmt):
                statement = args
                statement.accept(self)
            elif isinstance(args, expr.Expr):
                exp = args
                exp.accept(self)
        except ParseError as e:
            e.report()
            hadError = True

    def visitVariableExpr(self, exp):
        if (not len(self.scopes) == 0) and self.scopes[len(self.scopes)-1].get(exp.name.lexeme) == False:
            raise ParseError(
                exp.name, "Can't read local variable in its own initializer.")
        self.resolveLocal(exp, exp.name)

    def visitAssignExpr(self, exp):
        self.resolve(exp.value)
        self.resolveLocal(exp, exp.name)

    def visitFunctionStmt(self, statement):
        self.declare(statement.name)
        self.define(statement.name)

        self.resolveFunction(statement, FunctionType.FUNCTION)

    def visitExpressionStmt(self, statement):
        self.resolve(statement.expression)

    def visitIfStmt(self, statement):
        self.resolve(statement.condition)
        self.resolve(statement.thenBranch)
        if statement.elseBranch != None:
            self.resolve(statement.elseBranch)

    def visitPrintStmt(self, statement):
        self.resolve(statement.expression)

    def visitReturnStmt(self, statement):
        if self.currentFunction == FunctionType.NONE:
            raise ParseError(statement.keyword,
                             "Can't return from top-level code.")
        if statement.value != None:
            self.resolve(statement.value)

    def visitWhileStmt(self, statement):
        self.resolve(statement.condition)
        self.resolve(statement.body)

    def visitBinaryExpr(self, exp):
        self.resolve(exp.left)
        self.resolve(exp.right)

    def visitCallExpr(self, exp):
        self.resolve(exp.callee)

        for argument in exp.arguments:
            self.resolve(argument)

    def visitGroupingExpr(self, exp):
        self.resolve(exp.expression)

    def visitLiteralExpr(self, exp):
        return None

    def visitLogicalExpr(self, exp):
        self.resolve(exp.left)
        self.resolve(exp.right)

    def visitUnaryExpr(self, exp):
        self.resolve(exp.right)

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def declare(self, name):
        if len(self.scopes) == 0:
            return
        if name.lexeme in self.scopes[len(self.scopes)-1]:
            raise ParseError(
                name, "Already variable with this name in this scope.")
        self.scopes[len(self.scopes)-1][name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return
        self.scopes[len(self.scopes)-1][name.lexeme] = True

    def resolveLocal(self, exp, name):
        for i in reversed(range(0, len(self.scopes))):
            if name.lexeme in self.scopes[i].keys():
                self.interpreter.resolve(exp, len(self.scopes)-1-i)
                return

    def resolveFunction(self, function, type_):
        enclosingFunction = self.currentFunction
        self.currentFunction = type_
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.endScope()
        self.currentFunction = enclosingFunction