from enum import Enum
from typing import Any


class TokenType(Enum):
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"

    IDENT = "IDENT"
    INT = "INT"
    FLOAT = "FLOAT"

    SUM = "SUM"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"

    EQ = "EQ"

    LT = "<"
    GT = ">"
    EQ_EQ = "=="
    NOT_EQ = "!="
    LT_EQ = "<="
    GT_EQ = ">="

    SEMICOLON = "SEMICOLON"
    COLON = "COLON"
    COMMA = "COMMA"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    AT = "AT"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"

    PLUS_PLUS = "PLUS_PLUS"
    MINUS_MINUS = "MINUS_MINUS"

    VAR = "VAR"
    FN = "FN"
    RETURN = "RETURN"
    IF = "IF"
    WHILE = "WHILE"
    FOR = "FOR"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"

    TYPE = "TYPE"


class Token:
    def __init__(self, type: TokenType, literal: Any, line: int, pos: int) -> None:
        self.pos = pos
        self.type = type
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"Token[{self.type} : {self.literal} : Line {self.line} : Pos {self.pos}]"

    def __repr__(self):
        return str(self)


KEYWORDS: dict[str, TokenType] = {
    "var": TokenType.VAR,
    "func": TokenType.FN,
    "ret": TokenType.RETURN,
    "if": TokenType.IF,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "else": TokenType.ELSE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE
}

TYPE_KEYWORDS: list[str] = ["int", "float"]


def lookup_ident(ident: str) -> TokenType:
    tt: TokenType | None = KEYWORDS.get(ident)

    if tt is not None:
        return tt

    if ident in TYPE_KEYWORDS:
        return TokenType.TYPE

    return TokenType.IDENT
