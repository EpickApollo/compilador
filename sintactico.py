class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errores = []
    
    def analizar(self):
        resultado = "Programa\n"
        indentacion = 1
        
        try:
            i = 0
            while i < len(self.tokens):
                token = self.tokens[i]
                
                if token.tipo == 'KEYWORD':
                    if token.valor in ['int', 'float', 'void', 'string', 'bool']:
                        resultado += self.analizar_declaracion(i, indentacion)
                        # Avanzar hasta el siguiente punto y coma
                        while i < len(self.tokens) and self.tokens[i].valor != ';':
                            i += 1
                    
                    elif token.valor == 'if':
                        resultado += self.analizar_if(i, indentacion)
                        # Avanzar hasta el cierre de llave
                        while i < len(self.tokens) and self.tokens[i].valor != '}':
                            i += 1
                    
                    elif token.valor == 'while':
                        resultado += self.analizar_while(i, indentacion)
                        # Avanzar hasta el cierre de llave
                        while i < len(self.tokens) and self.tokens[i].valor != '}':
                            i += 1
                    
                    elif token.valor == 'for':
                        resultado += self.analizar_for(i, indentacion)
                        # Avanzar hasta el cierre de llave
                        while i < len(self.tokens) and self.tokens[i].valor != '}':
                            i += 1
                
                elif token.tipo == 'IDENTIFIER':
                    if i + 1 < len(self.tokens) and self.tokens[i + 1].valor == '=':
                        resultado += self.analizar_asignacion(i, indentacion)
                        # Avanzar hasta el siguiente punto y coma
                        while i < len(self.tokens) and self.tokens[i].valor != ';':
                            i += 1
                
                i += 1
            
            if self.errores:
                resultado += "\n\nERRORES SINTÁCTICOS:\n"
                for error in self.errores:
                    resultado += f"  • {error}\n"
            
        except Exception as e:
            resultado += f"\nError durante el análisis sintáctico: {str(e)}"
        
        return resultado if resultado != "Programa\n" else "Sin estructura sintáctica válida"
    
    def analizar_declaracion(self, i, indentacion):
        resultado = "  " * indentacion + "├─ Declaración\n"
        indentacion += 1
        resultado += "  " * indentacion + f"├─ Tipo: {self.tokens[i].valor}\n"
        
        if i + 1 < len(self.tokens) and self.tokens[i + 1].tipo == 'IDENTIFIER':
            resultado += "  " * indentacion + f"├─ Identificador: {self.tokens[i + 1].valor}\n"
        
        # Buscar asignación si existe
        j = i + 2
        while j < len(self.tokens) and self.tokens[j].valor != ';':
            if self.tokens[j].valor == '=':
                resultado += "  " * indentacion + "├─ Asignación\n"
                indentacion += 1
                resultado += "  " * indentacion + "├─ Expresión\n"
                break
            j += 1
        
        return resultado
    
    def analizar_if(self, i, indentacion):
        resultado = "  " * indentacion + "├─ Estructura IF\n"
        indentacion += 1
        resultado += "  " * indentacion + "├─ Condición\n"
        
        # Buscar el cuerpo del if
        j = i + 1
        llaves_abiertas = 0
        while j < len(self.tokens):
            if self.tokens[j].valor == '{':
                llaves_abiertas += 1
            elif self.tokens[j].valor == '}':
                llaves_abiertas -= 1
                if llaves_abiertas == 0:
                    break
            j += 1
        
        return resultado
    
    def analizar_while(self, i, indentacion):
        resultado = "  " * indentacion + "├─ Bucle WHILE\n"
        indentacion += 1
        resultado += "  " * indentacion + "├─ Condición\n"
        return resultado
    
    def analizar_for(self, i, indentacion):
        resultado = "  " * indentacion + "├─ Bucle FOR\n"
        indentacion += 1
        resultado += "  " * indentacion + "├─ Inicialización\n"
        resultado += "  " * indentacion + "├─ Condición\n"
        resultado += "  " * indentacion + "├─ Incremento\n"
        return resultado
    
    def analizar_asignacion(self, i, indentacion):
        resultado = "  " * indentacion + "├─ Asignación\n"
        indentacion += 1
        resultado += "  " * indentacion + f"├─ Variable: {self.tokens[i].valor}\n"
        resultado += "  " * indentacion + "├─ Expresión\n"
        return resultado