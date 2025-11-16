class GeneradorCodigoIntermedio:
    def __init__(self, tokens):
        self.tokens = tokens
        self.codigo = []
        self.temp_counter = 1
        self.label_counter = 1
    
    def generar(self):
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            
            # Declaraciones
            if token.tipo == 'KEYWORD' and token.valor in ['int', 'float', 'string', 'bool']:
                if i + 1 < len(self.tokens) and self.tokens[i + 1].tipo == 'IDENTIFIER':
                    nombre = self.tokens[i + 1].valor
                    self.codigo.append(f"DECLARE {token.valor} {nombre}")
                    i += 1
            
            # Asignaciones
            elif token.tipo == 'IDENTIFIER' and i + 1 < len(self.tokens) and self.tokens[i + 1].valor == '=':
                var_nombre = token.valor
                j = i + 2
                expresion = []
                
                while j < len(self.tokens) and self.tokens[j].valor != ';':
                    if self.tokens[j].tipo != 'DELIMITER' or self.tokens[j].valor in ['(', ')']:
                        expresion.append(self.tokens[j])
                    j += 1
                
                # Generar código intermedio para la expresión
                codigo_expresion = self.generar_expresion(expresion)
                for linea in codigo_expresion:
                    self.codigo.append(linea)
                
                # Asignar el resultado a la variable
                if codigo_expresion:
                    self.codigo.append(f"{var_nombre} = {codigo_expresion[-1].split('=')[1].strip()}")
                
                i = j
            
            # Condicionales
            elif token.valor == 'if':
                l1 = f"L{self.label_counter}"
                l2 = f"L{self.label_counter + 1}"
                self.label_counter += 2
                
                # Generar condición
                j = i + 2  # Saltar 'if' y '('
                condicion = []
                while j < len(self.tokens) and self.tokens[j].valor != ')':
                    condicion.append(self.tokens[j])
                    j += 1
                
                codigo_condicion = self.generar_expresion(condicion)
                for linea in codigo_condicion:
                    self.codigo.append(linea)
                
                if codigo_condicion:
                    temp_cond = codigo_condicion[-1].split('=')[0].strip()
                    self.codigo.append(f"IF {temp_cond} GOTO {l1}")
                    self.codigo.append(f"GOTO {l2}")
                    self.codigo.append(f"{l1}:")
                    # Cuerpo del if
                    self.codigo.append(f"{l2}:")
                
                i = j
            
            # Bucles
            elif token.valor == 'while':
                l_start = f"L_WHILE_{self.label_counter}"
                l_body = f"L_BODY_{self.label_counter}"
                l_end = f"L_END_{self.label_counter}"
                self.label_counter += 1
                
                self.codigo.append(f"{l_start}:")
                
                # Generar condición
                j = i + 2  # Saltar 'while' y '('
                condicion = []
                while j < len(self.tokens) and self.tokens[j].valor != ')':
                    condicion.append(self.tokens[j])
                    j += 1
                
                codigo_condicion = self.generar_expresion(condicion)
                for linea in codigo_condicion:
                    self.codigo.append(linea)
                
                if codigo_condicion:
                    temp_cond = codigo_condicion[-1].split('=')[0].strip()
                    self.codigo.append(f"IF {temp_cond} GOTO {l_body}")
                    self.codigo.append(f"GOTO {l_end}")
                    self.codigo.append(f"{l_body}:")
                    # Cuerpo del while
                    self.codigo.append(f"GOTO {l_start}")
                    self.codigo.append(f"{l_end}:")
                
                i = j
            
            i += 1
        
        return '\n'.join(self.codigo) if self.codigo else 'Sin código intermedio generado'
    
    def generar_expresion(self, tokens_expresion):
        if not tokens_expresion:
            return []
        
        # Expresión simple
        if len(tokens_expresion) == 1:
            return [f"t{self.temp_counter} = {tokens_expresion[0].valor}"]
        
        # Expresión binaria
        if len(tokens_expresion) == 3:
            t1 = f"t{self.temp_counter}"
            self.temp_counter += 1
            return [f"{t1} = {tokens_expresion[0].valor} {tokens_expresion[1].valor} {tokens_expresion[2].valor}"]
        
        # Expresión más compleja - simplificada
        resultado = []
        temp_actual = None
        
        for i in range(0, len(tokens_expresion), 2):
            if i == 0:
                temp_actual = f"t{self.temp_counter}"
                self.temp_counter += 1
                resultado.append(f"{temp_actual} = {tokens_expresion[i].valor}")
            elif i + 1 < len(tokens_expresion):
                nuevo_temp = f"t{self.temp_counter}"
                self.temp_counter += 1
                resultado.append(f"{nuevo_temp} = {temp_actual} {tokens_expresion[i].valor} {tokens_expresion[i+1].valor}")
                temp_actual = nuevo_temp
        
        return resultado