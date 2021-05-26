#!/usr/bin/env python
# coding: utf-8

import os
import string
import re
import pprint
os.getcwd()

class Token(object):
    KEYWORD, ID, SYM, STRCONST, INTCONST, READCONST, ASSIGN, COLON, COMMA, SEMICOLON, DOT, EQ, NQ, LT, LTE, GT, GTE, QUOTE, INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, TERM, AND, OR, NOT = (
    'KEYWORD', 'ID', 'SYM', 'STRCONST', 'INTCONST', 'READCONST', "ASSIGN",
    "COLON", "COMMA", "SEMICOLON", "DOT", "EQ", "NQ", "LT", "LTE", "GT", "GTE","QUOTE", 'INTEGER', 'PLUS', 'MINUS', 'MUL',
    'DIV', '(', ')', 'EOF', 'TERM', 'AND', 'OR', 'NOT')

    KEYWORDS = ("PROGRAM", "VAR", "DIV", "INTEGER", "REAL", "BEGIN", "END",
            "PROCEDURE", "IF", "THEN", "ELSE", "WHILE", "REPEAT", "UNTIL", "WRITE", "WRITELN", "OR", "AND", "DIV", "MOD", "NOT", "TRUNC", "REAL", "DO")
    
    def __init__(self, type, value, line_no, col_no):
        self.type = type
        self.value = value
        self.line_no = line_no
        self.col_no = col_no - len(str(value))
#         self.position = pos
        self.inverse = False
        
        self.row = []
    

    def __str__(self):
        return 'Token({type}, {value}, {line_no}, {position})'.format(type=self.type,
                                               value=repr(self.value), line_no=self.line_no, position=self.col_no)

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "hello | world & (why | are | you)"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.col_no = 0
        self.current_char = self.text[self.pos]
        self.line_no = 0
        self.symbol_table = {}

    def error(self):
        raise Exception('Invalid character')

    def peek(self):
        if self.pos + 1 < len(self.text):
            return self.text[self.pos + 1]
        else:
            return None

    def advance(self):
        self.pos += 1
        self.col_no += 1
    
        if '\n'in [self.current_char]:
            self.line_no += 1
            self.col_no = 0
            
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def word(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalpha()
                                                 or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result.upper() in Token.KEYWORDS:
            return Token(Token.KEYWORD, str(result), self.line_no, self.col_no)
        else:
            self.symbol_table[str(result)] = self.pos
            return Token(Token.ID, str(result), self.line_no, self.col_no)

    def readStringConst(self):
        result = '"'
        self.advance()
        while self.current_char is not None:
            result += self.current_char
            if self.current_char == '"':
                self.advance()
                break
            self.advance()

        return Token(Token.STRCONST, str(result), self.line_no, self.col_no)
    
    def update_symbol_table(self):
        token_list = self.get_all_tokens()
        symbol_table = {}
        for i in range(0, len(token_list)):
#             print(token_list[i].value)
            if token_list[i].value == "PROGRAM".lower():
                symbol_table[token_list[i+1].value] = "PROGRAM"
            
            if token_list[i].value == ":":
                symbol_table[token_list[i-1].value] = token_list[i+1].value
        self.symbol_table = symbol_table
        return symbol_table
    
    def get_all_tokens(self):
        token_list = []
        temp_pos = self.pos
        temp_current_char = self.current_char
        temp_line_no = self.line_no
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line_no = 0
        token = self.get_next_token()
        while token.type != Token.EOF:
            token_list.append(token)
            token = self.get_next_token()
            
        self.pos = temp_pos
        self.current_char = temp_current_char
        self.line_no = temp_line_no
        return token_list
        
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(Token.INTCONST, self.integer(), self.line_no, self.col_no)

            if self.current_char.isalpha():
                #                 print('Got Identifier  ' + self.current_char)
                return self.word()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(Token.ASSIGN, ":=", self.line_no, self.col_no)

            if self.current_char == ':':
                self.advance()
                return Token(Token.COLON, ":", self.line_no, self.col_no)

            if self.current_char == ',':
                self.advance()
                return Token(Token.COMMA, ",", self.line_no, self.col_no)

            if self.current_char == ';':
                self.advance()
                return Token(Token.SEMICOLON, ";", self.line_no, self.col_no)

            if self.current_char == '.':
                self.advance()
                return Token(Token.DOT, ".", self.line_no, self.col_no)
            
            if self.current_char == '!':

                self.advance()
                return Token(Token.NOT, 'NOT', self.line_no, self.col_no)

            if self.current_char == '&':

                self.advance()
                return Token(Token.AND, 'AND', self.line_no, self.col_no)

            if self.current_char == '|':

                self.advance()
                return Token(Token.OR, 'OR', self.line_no, self.col_no)

            if self.current_char == '+':
                self.advance()
                return Token(Token.PLUS, '+', self.line_no, self.col_no)

            if self.current_char == '-':
                self.advance()
                return Token(Token.MINUS, '-', self.line_no, self.col_no)
            
            if self.current_char == '"':
                return self.readStringConst()

            if self.current_char == '*':
                self.advance()
                return Token(Token.MUL, '*', self.line_no, self.col_no)

            if self.current_char == '/':
                self.advance()
                return Token(Token.DIV, '/', self.line_no, self.col_no)

            if self.current_char == '=':
                self.advance()
                return Token(Token.EQ, "=", self.line_no, self.col_no)
            
            if self.current_char == '<' and self.peek() == '>':
                self.advance()
                self.advance()
                return Token(Token.NEQ, "<=", self.line_no, self.col_no)
            
            if self.current_char == '<':
                self.advance()
                return Token(Token.LT, "<", self.line_no, self.col_no)
            
            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(Token.LTE, "<=", self.line_no, self.col_no)
            
            if self.current_char == '>' :
                self.advance()
                return Token(Token.GT, ">", self.line_no, self.col_no)
            
            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(Token.GTE, ">=", self.line_no, self.col_no)
            
            if self.current_char == '(':
                self.advance()
                return Token(Token.LPAREN, '(', self.line_no, self.col_no)

            if self.current_char == ')':
                self.advance()
                return Token(Token.RPAREN, ')', self.line_no, self.col_no)
            print("before error ",self.current_char)
            self.error()

        return Token(Token.EOF, None, self.line_no, self.col_no)



