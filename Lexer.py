from Tokens import TokenType, Token, lookup_ident
from typing import Any


class Lexer:
    def __init__(self, code: str) -> None:

        self.code = code

        self.pos: int = -1
        self.read_pos: int = 0
        self.line: int = 1

        self.current_ch: None = None

        self.__read_ch()

    def __read_ch(self) -> None:
        if self.read_pos >= len(self.code):
            self.current_ch = None
        else:
            self.current_ch = self.code[self.read_pos]

        self.pos = self.read_pos
        self.read_pos += 1

    def __peek_ch(self) -> str | None:
        if self.read_pos >= len(self.code):
            return None
        return self.code[self.read_pos]

    def __skip_whitespace(self) -> None:
        while self.current_ch in [' ', '\t', '\n', '\r']:
            if self.current_ch == '\n':
                self.line += 1

            self.__read_ch()

    def __new_token(self, tt: TokenType, literal: Any) -> Token:
        return Token(type=tt, literal=literal, line=self.line, pos=self.pos)

    def __is_digit(self, ch: str) -> bool:
        return '0' <= ch <= '9'

    def __is_letter(self, ch: str) -> bool:
        return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'

    def __read_number(self) -> Token:
        start_pos = self.pos
        dot_count: int = 0

        output = ""

        while self.__is_digit(self.current_ch) or self.current_ch == '.':
            if self.current_ch == '.':
                dot_count += 1

            if dot_count > 1:
                print(f"Too many dots in number Line: {self.line} Pos: {self.pos}")
                return self.__new_token(TokenType.ILLEGAL, self.code[start_pos:self.pos])

            output += self.code[self.pos]
            self.__read_ch()

            if self.current_ch is None:
                break

        if dot_count == 0:
            return self.__new_token(TokenType.INT, int(output))
        else:
            return self.__new_token(TokenType.FLOAT, float(output))

    def __read_identifier(self) -> str:
        pos = self.pos
        while self.current_ch is not None and (self.__is_letter(self.current_ch) or self.current_ch.isalnum()):
            self.__read_ch()

        return self.code[pos:self.pos]

    def next_token(self) -> Token:
        tok: Token = None

        self.__skip_whitespace()

        match self.current_ch:
            case '+':
                if self.__peek_ch() == '+':
                    ch = self.current_ch
                    self.__read_ch()
                    tok = self.__new_token(TokenType.PLUS_PLUS, ch + self.current_ch)
                else:
                    tok = self.__new_token(TokenType.SUM, self.current_ch)
            case '-':
                if self.__peek_ch() == '-':
                    ch = self.current_ch
                    self.__read_ch()
                    tok = self.__new_token(TokenType.MINUS_MINUS, ch + self.current_ch)
                else:
                    tok = self.__new_token(TokenType.SUB, self.current_ch)
            case '*':
                tok = self.__new_token(TokenType.MUL, self.current_ch)
            case '/':
                tok = self.__new_token(TokenType.DIV, self.current_ch)
            case ',':
                tok = self.__new_token(TokenType.COMMA, self.current_ch)
            case '(':
                tok = self.__new_token(TokenType.LPAREN, self.current_ch)
            case ')':
                tok = self.__new_token(TokenType.RPAREN, self.current_ch)
            case '{':
                tok = self.__new_token(TokenType.LBRACE, self.current_ch)
            case '}':
                tok = self.__new_token(TokenType.RBRACE, self.current_ch)
            case ':':
                tok = self.__new_token(TokenType.COLON, self.current_ch)
            case ';':
                tok = self.__new_token(TokenType.SEMICOLON, self.current_ch)
            case '@':
                tok = self.__new_token(TokenType.AT, self.current_ch)
            case None:
                tok = self.__new_token(TokenType.EOF, "")
            case '<':
                if self.__peek_ch() == '=':
                    ch = self.current_ch
                    self.__read_ch()
                    tok = self.__new_token(TokenType.LT_EQ, ch + self.current_ch)
                else:
                    tok = self.__new_token(TokenType.LT, self.current_ch)
            case '>':
                if self.__peek_ch() == '=':
                    ch = self.current_ch
                    self.__read_ch()
                    tok = self.__new_token(TokenType.GT_EQ, ch + self.current_ch)
                else:
                    tok = self.__new_token(TokenType.GT, self.current_ch)
            case '=':
                if self.__peek_ch() == '=':
                    ch = self.current_ch
                    self.__read_ch()
                    tok = self.__new_token(TokenType.EQ_EQ, ch + self.current_ch)
                else:
                    tok = self.__new_token(TokenType.EQ, self.current_ch)
            case '!':
                if self.__peek_ch() == '=':
                    ch = self.current_ch
                    self.__read_ch()
                    tok = self.__new_token(TokenType.NOT_EQ, ch + self.current_ch)
                else:
                    tok = self.__new_token(TokenType.ILLEGAL, self.current_ch)
            case _:
                if self.__is_letter(self.current_ch):
                    literal: str = self.__read_identifier()
                    tt: TokenType = lookup_ident(literal)
                    tok = self.__new_token(tt=tt, literal=literal)
                    return tok

                elif self.__is_digit(self.current_ch):
                    tok = self.__read_number()
                    return tok
                else:
                    tok = self.__new_token(TokenType.ILLEGAL, self.current_ch)

        self.__read_ch()
        return tok
