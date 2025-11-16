class Symbol:
    def __init__(self, nombre, tipo, scope, linea, valor=None):
        self.nombre = nombre
        self.tipo = tipo
        self.scope = scope
        self.linea = linea
        self.valor = valor
    
    def __repr__(self):
        return f"{self.nombre} ({self.tipo}) - {self.scope} - línea {self.linea}"

class TablaSimbolos:
    def __init__(self):
        self.simbolos = []
        self.declarados = set()
    
    def construir(self, tokens):
        scope_actual = 'global'
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            # Cambio de scope por funciones
            if token.tipo == 'DELIMITER' and token.valor == '{':
                scope_actual = 'local'
            elif token.tipo == 'DELIMITER' and token.valor == '}':
                scope_actual = 'global'
            
            # Declaraciones de variables
            if token.tipo == 'KEYWORD' and token.valor in ['int', 'float', 'void', 'string', 'bool']:
                if i + 1 < len(tokens) and tokens[i + 1].tipo == 'IDENTIFIER':
                    nombre = tokens[i + 1].valor
                    if nombre not in self.declarados:
                        simbolo = Symbol(nombre, token.valor, scope_actual, token.linea)
                        self.simbolos.append(simbolo)
                        self.declarados.add(nombre)
            
            # Declaraciones de funciones
            if (token.tipo == 'KEYWORD' and token.valor in ['int', 'float', 'void', 'string', 'bool'] and
                i + 2 < len(tokens) and tokens[i + 1].tipo == 'IDENTIFIER' and
                tokens[i + 2].tipo == 'DELIMITER' and tokens[i + 2].valor == '('):
                
                nombre = tokens[i + 1].valor
                if nombre not in self.declarados:
                    simbolo = Symbol(nombre, f'function({token.valor})', 'global', token.linea)
                    self.simbolos.append(simbolo)
                    self.declarados.add(nombre)
            
            i += 1
        
        return self.simbolos
    
    def buscar(self, nombre):
        for simbolo in self.simbolos:
            if simbolo.nombre == nombre:
                return simbolo
        return None