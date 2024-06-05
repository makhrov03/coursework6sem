from abc import ABC, abstractmethod
from enum import Enum


class NodeType(Enum):
    Program = "Program"

    ExpressionStatement = "ExpressionStatement"
    VarStatement = "VarStatement"
    FunctionStatement = "FunctionStatement"
    BlockStatement = "BlockStatement"
    ReturnStatement = "ReturnStatement"
    AssignStatement = "AssignStatement"
    IfStatement = "IfStatement"
    WhileStatement = "WhileStatement"

    InfixExpression = "InfixExpression"
    CallExpression = "CallExpression"

    IntegerLiteral = "IntegerLiteral"
    FloatLiteral = "FloatLiteral"
    IdentifierLiteral = "IdentifierLiteral"
    BooleanLiteral = "BooleanLiteral"

    FunctionParameter = "FunctionParameter"


class Node(ABC):
    @abstractmethod
    def type(self) -> NodeType:
        pass

    @abstractmethod
    def json(self) -> dict:
        pass


class Statement(Node):
    pass


class Expression(Node):
    pass


class Program(Node):
    def __init__(self) -> None:
        self.statements: list[Statement] = []

    def type(self) -> NodeType:
        return NodeType.Program

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [{stmt.type().value: stmt.json()} for stmt in self.statements]
        }


class FunctionParameter(Expression):
    def __init__(self, name: str, value_type: str = None) -> None:
        self.name = name
        self.value_type = value_type

    def type(self) -> NodeType:
        return NodeType.FunctionParameter

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name,
            "value_type": self.value_type
        }


class ExpressionStatement(Statement):
    def __init__(self, expr: Expression = None) -> None:
        self.expr: Expression = expr

    def type(self) -> NodeType:
        return NodeType.ExpressionStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "expr": self.expr.json()
        }


class VarStatement(Statement):
    def __init__(self, name=None, value=None, value_type=None):
        self.name = name
        self.value = value
        self.value_type = value_type

    def type(self) -> NodeType:
        return NodeType.VarStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name.json(),
            "value": self.value.json(),
            "value_type": self.value_type
        }


class BlockStatement(Statement):
    def __init__(self, statements: list[Statement] = None) -> None:
        self.statements = statements if statements is not None else []

    def type(self) -> NodeType:
        return NodeType.BlockStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [stmt.json() for stmt in self.statements]
        }


class ReturnStatement(Statement):
    def __init__(self, return_value: Expression = None) -> None:
        self.return_value = return_value

    def type(self) -> NodeType:
        return NodeType.ReturnStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "return_value": self.return_value.json()
        }


class FunctionStatement(Statement):
    def __init__(self, parameters: list[FunctionParameter] = [], body: BlockStatement = None, name=None, return_type: str = None) -> None:
        self.parameters = parameters
        self.body = body
        self.name = name
        self.return_type = return_type

    def type(self) -> NodeType:
        return NodeType.FunctionStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name": self.name.json(),
            "return_type": self.return_type,
            "parameters": [param.json() for param in self.parameters],
            "body": self.body.json()
        }


class AssignStatement(Statement):
    def __init__(self, ident: Expression = None, right_value: Expression = None) -> None:
        self.ident = ident
        self.right_value = right_value

    def type(self) -> NodeType:
        return NodeType.AssignStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "ident": self.ident.json(),
            "right_value": self.right_value.json()
        }


class IfStatement(Statement):
    def __init__(self, condition: Expression = None, consequence: BlockStatement = None, alternative: BlockStatement = None) -> None:
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def type(self) -> NodeType:
        return NodeType.IfStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "condition": self.condition.json(),
            "consequence": self.consequence.json(),
            "alternative": self.alternative.json() if self.alternative is not None else None
        }


class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: BlockStatement = None) -> None:
        self.condition = condition
        self.body = body if body is not None else []

    def type(self) -> NodeType:
        return NodeType.WhileStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "condition": self.condition.json(),
            "body": self.body.json()
        }


class InfixExpression(Expression):
    def __init__(self, left_node: Expression, operator: str, right_node: Expression = None):
        self.left_node: Expression = left_node
        self.operator: str = operator
        self.right_node: Expression = right_node

    def type(self) -> NodeType:
        return NodeType.InfixExpression

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "left_node": self.left_node.json(),
            "operator": self.operator,
            "right_node": self.right_node.json()
        }


class CallExpression(Expression):
    def __init__(self, function: Expression = None, arguments: list[Expression] = None) -> None:
        self.function = function
        self.arguments = arguments

    def type(self) -> NodeType:
        return NodeType.CallExpression

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "function": self.function.json(),
            "arguments": [arg.json() for arg in self.arguments]
        }


class IntegerLiteral(Expression):
    def __init__(self, value: int = None):
        self.value: int = value

    def type(self) -> NodeType:
        return NodeType.IntegerLiteral

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }


class FloatLiteral(Expression):
    def __init__(self, value: float = None):
        self.value: float = value

    def type(self) -> NodeType:
        return NodeType.FloatLiteral

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }


class IdentifierLiteral(Expression):
    def __init__(self, value: str = None):
        self.value: str = value

    def type(self) -> NodeType:
        return NodeType.IdentifierLiteral

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }


class BooleanLiteral(Expression):
    def __init__(self, value: bool = None):
        self.value: bool = value

    def type(self) -> NodeType:
        return NodeType.BooleanLiteral

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }
