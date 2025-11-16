class Traductor:
    def __init__(self, tokens, lenguaje_destino="python"):
        self.tokens = tokens
        self.lenguaje_destino = lenguaje_destino
        self.codigo_traducido = []
        self.indentacion = 0
    
    def traducir(self):
        if self.lenguaje_destino == "python":
            return self.traducir_a_python()
        elif self.lenguaje_destino == "javascript":
            return self.traducir_a_javascript()
        elif self.lenguaje_destino == "java":
            return self.traducir_a_java()
        else:
            return "Lenguaje destino no soportado"
    
    def traducir_a_python(self):
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            
            # Declaraciones de variables
            if token.tipo == 'KEYWORD' and token.valor in ['int', 'float', 'string', 'bool']:
                if i + 1 < len(self.tokens) and self.tokens[i + 1].tipo == 'IDENTIFIER':
                    nombre = self.tokens[i + 1].valor
                    # En Python no se declaran tipos explícitamente
                    if i + 2 < len(self.tokens) and self.tokens[i + 2].valor == '=':
                        valor = self.obtener_valor_asignacion(i + 3)
                        self.codigo_traducido.append(f"{nombre} = {valor}")
                        i += 3
                    else:
                        self.codigo_traducido.append(f"{nombre} = None")
                    i += 1
            
            # Asignaciones
            elif token.tipo == 'IDENTIFIER' and i + 1 < len(self.tokens) and self.tokens[i + 1].valor == '=':
                nombre = token.valor
                valor = self.obtener_valor_asignacion(i + 2)
                self.codigo_traducido.append(f"{nombre} = {valor}")
                # Avanzar hasta el punto y coma
                while i < len(self.tokens) and self.tokens[i].valor != ';':
                    i += 1
            
            # Estructuras de control
            elif token.valor == 'if':
                condicion = self.obtener_condicion(i + 2)
                self.codigo_traducido.append(f"if {condicion}:")
                self.indentacion += 1
                # Buscar el cuerpo
                j = i + 1
                while j < len(self.tokens) and self.tokens[j].valor != '{':
                    j += 1
                i = j
            
            elif token.valor == 'while':
                condicion = self.obtener_condicion(i + 2)
                self.codigo_traducido.append(f"while {condicion}:")
                self.indentacion += 1
                # Buscar el cuerpo
                j = i + 1
                while j < len(self.tokens) and self.tokens[j].valor != '{':
                    j += 1
                i = j
            
            elif token.valor == 'for':
                # Simplificación del for
                self.codigo_traducido.append("# For loop - necesita traducción manual")
                # Buscar el cuerpo
                j = i + 1
                while j < len(self.tokens) and self.tokens[j].valor != '{':
                    j += 1
                i = j
            
            # Llaves - manejar indentación
            elif token.valor == '{':
                self.indentacion += 1
            elif token.valor == '}':
                self.indentacion -= 1
            
            i += 1
        
        # Aplicar indentación
        codigo_final = []
        for linea in self.codigo_traducido:
            codigo_final.append("    " * self.indentacion + linea)
        
        return '\n'.join(codigo_final) if codigo_final else "No se pudo traducir el código"
    
    def traducir_a_javascript(self):
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            
            # Declaraciones de variables
            if token.tipo == 'KEYWORD' and token.valor in ['int', 'float', 'string', 'bool']:
                if i + 1 < len(self.tokens) and self.tokens[i + 1].tipo == 'IDENTIFIER':
                    nombre = self.tokens[i + 1].valor
                    # En JavaScript usamos let/const
                    if i + 2 < len(self.tokens) and self.tokens[i + 2].valor == '=':
                        valor = self.obtener_valor_asignacion(i + 3)
                        self.codigo_traducido.append(f"let {nombre} = {valor}")
                        i += 3
                    else:
                        self.codigo_traducido.append(f"let {nombre}")
                    i += 1
            
            # Asignaciones
            elif token.tipo == 'IDENTIFIER' and i + 1 < len(self.tokens) and self.tokens[i + 1].valor == '=':
                nombre = token.valor
                valor = self.obtener_valor_asignacion(i + 2)
                self.codigo_traducido.append(f"{nombre} = {valor}")
                # Avanzar hasta el punto y coma
                while i < len(self.tokens) and self.tokens[i].valor != ';':
                    i += 1
            
            # Estructuras de control (similar a Python)
            elif token.valor == 'if':
                condicion = self.obtener_condicion(i + 2)
                self.codigo_traducido.append(f"if ({condicion}) {{")
                self.indentacion += 1
            
            elif token.valor == 'while':
                condicion = self.obtener_condicion(i + 2)
                self.codigo_traducido.append(f"while ({condicion}) {{")
                self.indentacion += 1
            
            elif token.valor == 'for':
                self.codigo_traducido.append("// For loop - necesita traducción manual")
                # Buscar el cuerpo
                j = i + 1
                while j < len(self.tokens) and self.tokens[j].valor != '{':
                    j += 1
                i = j
            
            # Llaves - manejar indentación
            elif token.valor == '{':
                if self.codigo_traducido and '{' not in self.codigo_traducido[-1]:
                    self.codigo_traducido.append("{")
                self.indentacion += 1
            elif token.valor == '}':
                self.indentacion -= 1
                self.codigo_traducido.append("}")
            
            i += 1
        
        # Aplicar indentación
        codigo_final = []
        for linea in self.codigo_traducido:
            if linea.endswith('{') or linea == '}':
                codigo_final.append("    " * (self.indentacion if not linea.endswith('{') else self.indentacion - 1) + linea)
            else:
                codigo_final.append("    " * self.indentacion + linea)
        
        return '\n'.join(codigo_final) if codigo_final else "No se pudo traducir el código"
    
    def traducir_a_java(self):
        i = 0
        clase_principal = False
        
        while i < len(self.tokens):
            token = self.tokens[i]
            
            # Declaraciones de variables
            if token.tipo == 'KEYWORD' and token.valor in ['int', 'float', 'string', 'bool']:
                if i + 1 < len(self.tokens) and self.tokens[i + 1].tipo == 'IDENTIFIER':
                    nombre = self.tokens[i + 1].valor
                    tipo_java = self.convertir_tipo(token.valor)
                    
                    if i + 2 < len(self.tokens) and self.tokens[i + 2].valor == '=':
                        valor = self.obtener_valor_asignacion(i + 3)
                        self.codigo_traducido.append(f"{tipo_java} {nombre} = {valor};")
                        i += 3
                    else:
                        self.codigo_traducido.append(f"{tipo_java} {nombre};")
                    i += 1
            
            # Asignaciones
            elif token.tipo == 'IDENTIFIER' and i + 1 < len(self.tokens) and self.tokens[i + 1].valor == '=':
                nombre = token.valor
                valor = self.obtener_valor_asignacion(i + 2)
                self.codigo_traducido.append(f"{nombre} = {valor};")
                # Avanzar hasta el punto y coma
                while i < len(self.tokens) and self.tokens[i].valor != ';':
                    i += 1
            
            # Estructuras de control
            elif token.valor == 'if':
                condicion = self.obtener_condicion(i + 2)
                self.codigo_traducido.append(f"if ({condicion}) {{")
                self.indentacion += 1
            
            elif token.valor == 'while':
                condicion = self.obtener_condicion(i + 2)
                self.codigo_traducido.append(f"while ({condicion}) {{")
                self.indentacion += 1
            
            elif token.valor == 'for':
                self.codigo_traducido.append("// For loop - necesita traducción manual")
                # Buscar el cuerpo
                j = i + 1
                while j < len(self.tokens) and self.tokens[j].valor != '{':
                    j += 1
                i = j
            
            # Función main para Java
            elif (token.tipo == 'KEYWORD' and token.valor in ['int', 'void'] and
                  i + 1 < len(self.tokens) and self.tokens[i + 1].valor == 'main'):
                self.codigo_traducido.insert(0, "public class Main {")
                self.codigo_traducido.insert(1, "    public static void main(String[] args) {")
                self.indentacion += 2
                clase_principal = True
                i += 1
            
            # Llaves - manejar indentación
            elif token.valor == '{':
                if self.codigo_traducido and '{' not in self.codigo_traducido[-1]:
                    self.codigo_traducido.append("{")
                self.indentacion += 1
            elif token.valor == '}':
                self.indentacion -= 1
                self.codigo_traducido.append("}")
            
            i += 1
        
        # Cerrar clase principal si se abrió
        if clase_principal:
            self.codigo_traducido.append("    }")
            self.codigo_traducido.append("}")
        
        # Aplicar indentación
        codigo_final = []
        for linea in self.codigo_traducido:
            if linea.endswith('{') or linea == '}':
                codigo_final.append("    " * (self.indentacion if not linea.endswith('{') else self.indentacion - 1) + linea)
            else:
                codigo_final.append("    " * self.indentacion + linea)
        
        return '\n'.join(codigo_final) if codigo_final else "No se pudo traducir el código"
    
    def obtener_valor_asignacion(self, inicio):
        valores = []
        i = inicio
        while i < len(self.tokens) and self.tokens[i].valor != ';':
            valores.append(self.tokens[i].valor)
            i += 1
        return ' '.join(valores)
    
    def obtener_condicion(self, inicio):
        condicion = []
        i = inicio
        while i < len(self.tokens) and self.tokens[i].valor != ')':
            condicion.append(self.tokens[i].valor)
            i += 1
        return ' '.join(condicion)
    
    def convertir_tipo(self, tipo_original):
        conversiones = {
            'int': 'int',
            'float': 'float',
            'string': 'String',
            'bool': 'boolean',
            'void': 'void'
        }
        return conversiones.get(tipo_original, tipo_original)