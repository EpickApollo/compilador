class AnalizadorSemantico:
    def __init__(self, tokens, tabla_simbolos):
        self.tokens = tokens
        self.tabla = tabla_simbolos
        self.errores = []
        self.advertencias = []
    
    def analizar(self):
        declarados = set(s.nombre for s in self.tabla.simbolos)
        usados = set()
        
        for i in range(len(self.tokens)):
            token = self.tokens[i]
            
            # Verificar uso de variables no declaradas
            if token.tipo == 'IDENTIFIER':
                prev_token = self.tokens[i - 1] if i > 0 else None
                
                # Si no es una declaración
                if not prev_token or prev_token.valor not in ['int', 'float', 'void', 'string', 'bool']:
                    if token.valor not in declarados:
                        self.errores.append(f"Error línea {token.linea}: Variable '{token.valor}' no declarada")
                    else:
                        usados.add(token.valor)
            
            # Verificar división por cero
            if token.tipo == 'OPERATOR' and token.valor == '/':
                if i + 1 < len(self.tokens):
                    next_token = self.tokens[i + 1]
                    if next_token.tipo == 'INTEGER' and next_token.valor == '0':
                        self.advertencias.append(f"Advertencia línea {token.linea}: Posible división por cero")
            
            # Verificar tipos en operaciones
            if token.tipo == 'OPERATOR' and token.valor in ['+', '-', '*', '/']:
                if i > 0 and i + 1 < len(self.tokens):
                    left = self.tokens[i - 1]
                    right = self.tokens[i + 1]
                    
                    # Verificar operaciones entre tipos incompatibles
                    if (left.tipo == 'STRING' and right.tipo != 'STRING' and token.valor == '+'):
                        self.advertencias.append(f"Advertencia línea {token.linea}: Concatenación de string con tipo no string")
        
        # Variables no usadas
        for simbolo in self.tabla.simbolos:
            if simbolo.nombre not in usados and simbolo.tipo.startswith('function'):
                self.advertencias.append(f"Advertencia: Función '{simbolo.nombre}' declarada pero no usada")
            elif simbolo.nombre not in usados:
                self.advertencias.append(f"Advertencia: Variable '{simbolo.nombre}' declarada pero no usada")
        
        resultado = "=== ANÁLISIS SEMÁNTICO ===\n\n"
        
        if not self.errores and not self.advertencias:
            resultado += "✓ No se encontraron errores semánticos\n"
            resultado += "✓ Todas las variables están correctamente declaradas\n"
            resultado += "✓ No hay advertencias de tipos\n"
        else:
            if self.errores:
                resultado += "ERRORES:\n"
                for error in self.errores:
                    resultado += f"  • {error}\n"
                resultado += "\n"
            
            if self.advertencias:
                resultado += "ADVERTENCIAS:\n"
                for adv in self.advertencias:
                    resultado += f"  • {adv}\n"
        
        return resultado