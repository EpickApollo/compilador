import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from lexico import AnalizadorLexico, Token
from simbolos import TablaSimbolos
from sintactico import AnalizadorSintactico
from semantico import AnalizadorSemantico
from intermedio import GeneradorCodigoIntermedio
from traductor import Traductor

class CompiladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Moderno - Python")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2b2b2b')
        
        # Variables para modo oscuro/claro
        self.modo_oscuro = True
        self.colores_claro = {
            'bg': '#f8f9fa',
            'fg': '#212529',
            'editor_bg': '#ffffff',
            'output_bg': '#ffffff',
            'btn_bg': '#e9ecef',
            'btn_fg': '#212529',
            'accent': '#007bff',
            'header_bg': '#343a40',
            'header_fg': '#ffffff'
        }
        self.colores_oscuro = {
            'bg': '#1e1e1e',
            'fg': '#d4d4d4',
            'editor_bg': '#2d2d2d',
            'output_bg': '#252526',
            'btn_bg': '#3c3c3c',
            'btn_fg': '#cccccc',
            'accent': '#0d6efd',
            'header_bg': '#2d2d30',
            'header_fg': '#ffffff'
        }
        
        self.crear_interfaz()
        self.aplicar_tema()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header moderno
        header = tk.Frame(main_frame, height=70)
        header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header, text="🚀 COMPILADOR MODERNO", 
                font=('Segoe UI', 20, 'bold')).pack(side=tk.LEFT, padx=15)
        
        # Botones de control en header
        control_frame = tk.Frame(header)
        control_frame.pack(side=tk.RIGHT, padx=10)
        
        self.btn_tema = tk.Button(control_frame, text="☀️", font=('Arial', 14), 
                                 command=self.cambiar_tema, width=3, relief='flat')
        self.btn_tema.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="📊 Estadísticas", font=('Segoe UI', 10),
                 command=self.mostrar_estadisticas, relief='flat').pack(side=tk.LEFT, padx=5)
        
        # Contenedor principal
        container = tk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Editor
        left_panel = tk.Frame(container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Header del editor
        editor_header = tk.Frame(left_panel)
        editor_header.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(editor_header, text="📝 Editor de Código", 
                font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        # Botones del editor
        btn_frame = tk.Frame(editor_header)
        btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(btn_frame, text="📄 Ejemplo", command=self.cargar_ejemplo, 
                 font=('Segoe UI', 9), relief='flat').pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🗑️ Limpiar", command=self.limpiar,
                 font=('Segoe UI', 9), relief='flat').pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="💾 Guardar", command=self.guardar_archivo,
                 font=('Segoe UI', 9), relief='flat').pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="📂 Abrir", command=self.abrir_archivo,
                 font=('Segoe UI', 9), relief='flat').pack(side=tk.LEFT, padx=2)

        tk.Button(btn_frame, text="📖 Documentación", command=self.mostrar_documentacion,
         font=('Segoe UI', 9), relief='flat').pack(side=tk.LEFT, padx=2)
        
        # Editor de código con números de línea
        editor_container = tk.Frame(left_panel)
        editor_container.pack(fill=tk.BOTH, expand=True)
        
        # Números de línea
        self.line_numbers = scrolledtext.ScrolledText(editor_container, width=4, padx=3, 
                                                     takefocus=0, border=0, 
                                                     background='#f0f0f0', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor principal
        self.editor = scrolledtext.ScrolledText(editor_container, wrap=tk.WORD, 
                                               font=('Consolas', 11), undo=True)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar números de línea
        self.actualizar_numeros_linea()
        self.editor.bind('<KeyRelease>', self.on_editor_change)
        
        # Panel de compilación
        compile_frame = tk.Frame(left_panel)
        compile_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Selector de lenguaje para traducción
        lang_frame = tk.Frame(compile_frame)
        lang_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(lang_frame, text="Traducir a:", font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.lang_var = tk.StringVar(value="python")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                 values=["python", "javascript", "java"], 
                                 state="readonly", width=12)
        lang_combo.pack(side=tk.LEFT)
        
        # Botón compilar
        self.btn_compilar = tk.Button(compile_frame, text="▶ COMPILAR Y TRADUCIR", 
                                     command=self.compilar, 
                                     font=('Segoe UI', 11, 'bold'),
                                     height=2, bg='#28a745', fg='white',
                                     relief='flat')
        self.btn_compilar.pack(side=tk.RIGHT, fill=tk.X, padx=(10, 0))
        
        # Panel derecho - Resultados
        right_panel = tk.Frame(container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right_panel, text="📊 Resultados", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        # Notebook para pestañas
        style = ttk.Style()
        style.configure("Custom.TNotebook", background=self.colores_oscuro['bg'])
        style.configure("Custom.TNotebook.Tab", background=self.colores_oscuro['btn_bg'], 
                       foreground=self.colores_oscuro['fg'])
        
        self.notebook = ttk.Notebook(right_panel, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear pestañas
        self.tabs = {}
        pestanas = [
            ('📋 Salida', 'salida'),
            ('🔤 Tokens', 'tokens'),
            ('📚 Símbolos', 'simbolos'),
            ('🌳 Sintaxis', 'sintaxis'),
            ('🔍 Semántica', 'semantica'),
            ('⚡ Cód. Intermedio', 'intermedio'),
            ('🌐 Traducción', 'traduccion')
        ]
        
        for titulo, clave in pestanas:
            frame = tk.Frame(self.notebook)
            self.notebook.add(frame, text=titulo)
            
            text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                                   font=('Consolas', 10))
            text_widget.pack(fill=tk.BOTH, expand=True)
            self.tabs[clave] = text_widget
    
    def aplicar_tema(self):
        colores = self.colores_oscuro if self.modo_oscuro else self.colores_claro
        
        self.root.configure(bg=colores['bg'])
        
        # Actualizar todos los widgets
        for widget in self.root.winfo_children():
            self.actualizar_widget_tema(widget, colores)
        
        # Editor y outputs
        self.editor.configure(bg=colores['editor_bg'], fg=colores['fg'], 
                             insertbackground=colores['fg'],
                             selectbackground=colores['accent'])
        
        self.line_numbers.configure(bg=colores['btn_bg'], fg=colores['fg'])
        
        for tab in self.tabs.values():
            tab.configure(bg=colores['output_bg'], fg=colores['fg'],
                         insertbackground=colores['fg'])
        
        self.btn_tema.configure(text="☀️" if self.modo_oscuro else "🌙")
        
        # Configurar estilo de notebook
        style = ttk.Style()
        style.configure("Custom.TNotebook", background=colores['bg'])
        style.configure("Custom.TNotebook.Tab", 
                       background=colores['btn_bg'], 
                       foreground=colores['fg'])
    
    def actualizar_widget_tema(self, widget, colores):
        try:
            if isinstance(widget, (tk.Frame, tk.Label)):
                widget.configure(bg=colores['bg'], fg=colores['fg'])
            elif isinstance(widget, tk.Button) and widget != self.btn_compilar:
                widget.configure(bg=colores['btn_bg'], fg=colores['fg'],
                                relief='flat')
        except:
            pass
        
        for child in widget.winfo_children():
            self.actualizar_widget_tema(child, colores)
    
    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_tema()
    
    def actualizar_numeros_linea(self):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        
        line_count = self.editor.get('1.0', tk.END).count('\n')
        line_numbers_text = '\n'.join(str(i) for i in range(1, line_count + 2))
        self.line_numbers.insert('1.0', line_numbers_text)
        self.line_numbers.config(state='disabled')
    
    def on_editor_change(self, event=None):
        self.actualizar_numeros_linea()
    
    def mostrar_documentacion(self):
        import webbrowser
        import os
    
        doc_path = os.path.join(os.path.dirname(__file__), "documentacion_tecnica.html")
        webbrowser.open(f"file://{doc_path}")

    def cargar_ejemplo(self):
        ejemplo = """// Ejemplo de código en C-like
int main() {
    // Declaración de variables
    int x = 10;
    float y = 3.14;
    string nombre = "Mundo";
    bool activo = true;
    
    // Estructuras de control
    if (x > 5) {
        printf("x es mayor que 5\\n");
    } else {
        printf("x es menor o igual a 5\\n");
    }
    
    // Bucle while
    int i = 0;
    while (i < 5) {
        printf("Iteración: %d\\n", i);
        i = i + 1;
    }
    
    // Bucle for
    for (int j = 0; j < 3; j = j + 1) {
        printf("For loop: j = %d\\n", j);
    }
    
    // Operaciones matemáticas
    float resultado = x * y + 2.5;
    
    return 0;
}"""
        self.editor.delete('1.0', tk.END)
        self.editor.insert('1.0', ejemplo)
        self.actualizar_numeros_linea()
    
    def limpiar(self):
        self.editor.delete('1.0', tk.END)
        for tab in self.tabs.values():
            tab.delete('1.0', tk.END)
        self.actualizar_numeros_linea()
    
    def guardar_archivo(self):
        from tkinter import filedialog
        archivo = filedialog.asksaveasfilename(
            defaultextension=".c",
            filetypes=[("Archivos C", "*.c"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            with open(archivo, 'w') as f:
                f.write(self.editor.get('1.0', tk.END))
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente")
    
    def abrir_archivo(self):
        from tkinter import filedialog
        archivo = filedialog.askopenfilename(
            filetypes=[("Archivos C", "*.c"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            with open(archivo, 'r') as f:
                contenido = f.read()
            self.editor.delete('1.0', tk.END)
            self.editor.insert('1.0', contenido)
            self.actualizar_numeros_linea()
    
    def mostrar_estadisticas(self):
        codigo = self.editor.get('1.0', tk.END)
        lineas = codigo.count('\n')
        palabras = len(codigo.split())
        caracteres = len(codigo)
        
        stats = f"""📊 Estadísticas del Código:

• Líneas de código: {lineas}
• Palabras: {palabras}
• Caracteres: {caracteres}
• Tamaño: {caracteres / 1024:.2f} KB

Características detectadas:
• Variables: {len([w for w in codigo.split() if w in ['int', 'float', 'string', 'bool']])}
• Bucles: {codigo.count('while') + codigo.count('for')}
• Condicionales: {codigo.count('if')}
• Funciones: {codigo.count('(') - codigo.count(';')}"""

        messagebox.showinfo("Estadísticas", stats)
    
    def compilar(self):
        # Limpiar outputs
        for tab in self.tabs.values():
            tab.delete('1.0', tk.END)
        
        codigo = self.editor.get('1.0', tk.END)
        
        if not codigo.strip():
            self.tabs['salida'].insert('1.0', "❌ Error: No hay código fuente para compilar")
            return
        
        try:
            # Análisis Léxico
            lexico = AnalizadorLexico(codigo)
            tokens = lexico.analizar()
            
            salida_tokens = "=== TOKENS GENERADOS ===\n\n"
            for token in tokens:
                salida_tokens += f"{token}\n"
            self.tabs['tokens'].insert('1.0', salida_tokens if salida_tokens else "Sin tokens")
            
            # Tabla de Símbolos
            tabla = TablaSimbolos()
            simbolos = tabla.construir(tokens)
            
            salida_simbolos = "=== TABLA DE SÍMBOLOS ===\n\n"
            salida_simbolos += "Nombre\t\tTipo\t\tÁmbito\t\tLínea\n"
            salida_simbolos += "-" * 60 + "\n"
            for simbolo in simbolos:
                salida_simbolos += f"{simbolo.nombre}\t\t{simbolo.tipo}\t\t{simbolo.scope}\t\t{simbolo.linea}\n"
            self.tabs['simbolos'].insert('1.0', salida_simbolos if simbolos else "Sin símbolos")
            
            # Análisis Sintáctico
            sintactico = AnalizadorSintactico(tokens)
            arbol = sintactico.analizar()
            self.tabs['sintaxis'].insert('1.0', arbol)
            
            # Análisis Semántico
            semantico = AnalizadorSemantico(tokens, tabla)
            resultado_semantico = semantico.analizar()
            self.tabs['semantica'].insert('1.0', resultado_semantico)
            
            # Código Intermedio
            generador = GeneradorCodigoIntermedio(tokens)
            codigo_intermedio = generador.generar()
            self.tabs['intermedio'].insert('1.0', codigo_intermedio)
            
            # Traducción
            lenguaje_destino = self.lang_var.get()
            traductor = Traductor(tokens, lenguaje_destino)
            codigo_traducido = traductor.traducir()
            
            salida_traduccion = f"=== TRADUCCIÓN A {lenguaje_destino.upper()} ===\n\n"
            salida_traduccion += codigo_traducido
            self.tabs['traduccion'].insert('1.0', salida_traduccion)
            
            # Salida general
            if not semantico.errores:
                self.tabs['salida'].insert('1.0', 
                    "✅ Compilación completada exitosamente\n\n"
                    f"📊 Estadísticas:\n"
                    f"   • Tokens generados: {len(tokens)}\n"
                    f"   • Símbolos en tabla: {len(simbolos)}\n"
                    f"   • Errores semánticos: 0\n"
                    f"   • Advertencias: {len(semantico.advertencias)}\n"
                    f"   • Traducido a: {lenguaje_destino}\n\n"
                    "💡 Revisa las pestañas para ver los detalles de cada fase.")
            else:
                self.tabs['salida'].insert('1.0', 
                    f"⚠️ Compilación con errores\n\n"
                    f"📊 Estadísticas:\n"
                    f"   • Errores encontrados: {len(semantico.errores)}\n"
                    f"   • Advertencias: {len(semantico.advertencias)}\n\n"
                    "❌ Revisa la pestaña 'Semántica' para más detalles.")
            
        except Exception as e:
            self.tabs['salida'].insert('1.0', 
                f"❌ Error durante la compilación:\n{str(e)}\n\n"
                "💡 Verifica que el código sea válido y vuelve a intentar.")