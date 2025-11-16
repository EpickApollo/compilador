import re

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
    
    def __repr__(self):
        return f"{self.tipo}: {self.valor} (línea {self.linea})"

class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []
        self.pos = 0
        self.linea = 1
        self.keywords = ['int', 'float', 'if', 'else', 'while', 'return', 'void', 'for', 'string', 'bool', 'true', 'false']
        self.operadores = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!']
        self.delimitadores = [';', ',', '(', ')', '{', '}', '[', ']']
    
    def analizar(self):
        while self.pos < len(self.codigo):
            char = self.codigo[self.pos]
            
            # Espacios en blanco
            if char in ' \t':
                self.pos += 1
                continue
            
            # Nueva línea
            if char == '\n':
                self.linea += 1
                self.pos += 1
                continue
            
            # Comentarios de línea
            if char == '/' and self.pos + 1 < len(self.codigo) and self.codigo[self.pos + 1] == '/':
                while self.pos < len(self.codigo) and self.codigo[self.pos] != '\n':
                    self.pos += 1
                continue
            
            # Comentarios de bloque
            if char == '/' and self.pos + 1 < len(self.codigo) and self.codigo[self.pos + 1] == '*':
                self.pos += 2
                while (self.pos < len(self.codigo) and 
                       not (self.codigo[self.pos] == '*' and self.pos + 1 < len(self.codigo) and 
                            self.codigo[self.pos + 1] == '/')):
                    if self.codigo[self.pos] == '\n':
                        self.linea += 1
                    self.pos += 1
                self.pos += 2
                continue
            
            # Identificadores y palabras clave
            if char.isalpha() or char == '_':
                palabra = self.leer_palabra()
                tipo = 'KEYWORD' if palabra in self.keywords else 'IDENTIFIER'
                self.tokens.append(Token(tipo, palabra, self.linea))
                continue
            
            # Números
            if char.isdigit():
                numero = self.leer_numero()
                tipo = 'FLOAT' if '.' in numero else 'INTEGER'
                self.tokens.append(Token(tipo, numero, self.linea))
                continue
            
            # Strings
            if char == '"':
                string_val = self.leer_string()
                self.tokens.append(Token('STRING', string_val, self.linea))
                continue
            
            # Operadores de dos caracteres
            if self.pos + 1 < len(self.codigo):
                dos_chars = self.codigo[self.pos:self.pos + 2]
                if dos_chars in ['==', '!=', '<=', '>=', '++', '--', '&&', '||']:
                    self.tokens.append(Token('OPERATOR', dos_chars, self.linea))
                    self.pos += 2
                    continue
            
            # Operadores simples
            if char in self.operadores:
                self.tokens.append(Token('OPERATOR', char, self.linea))
                self.pos += 1
                continue
            
            # Delimitadores
            if char in self.delimitadores:
                self.tokens.append(Token('DELIMITER', char, self.linea))
                self.pos += 1
                continue
            
            # Carácter no reconocido
            self.tokens.append(Token('ERROR', char, self.linea))
            self.pos += 1
        
        return self.tokens
    
    def leer_palabra(self):
        inicio = self.pos
        while self.pos < len(self.codigo) and (self.codigo[self.pos].isalnum() or self.codigo[self.pos] == '_'):
            self.pos += 1
        return self.codigo[inicio:self.pos]
    
    def leer_numero(self):
        inicio = self.pos
        tiene_punto = False
        while self.pos < len(self.codigo) and (self.codigo[self.pos].isdigit() or self.codigo[self.pos] == '.'):
            if self.codigo[self.pos] == '.':
                if tiene_punto:
                    break
                tiene_punto = True
            self.pos += 1
        return self.codigo[inicio:self.pos]
    
    def leer_string(self):
        self.pos += 1  # Saltar la comilla inicial
        inicio = self.pos
        while self.pos < len(self.codigo) and self.codigo[self.pos] != '"':
            if self.codigo[self.pos] == '\\':  # Manejar caracteres escapados
                self.pos += 1
            self.pos += 1
        string_val = self.codigo[inicio:self.pos]
        self.pos += 1  # Saltar la comilla final
        return string_val