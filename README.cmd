compilador/
├── main.py                 # Punto de entrada principal
├── gui.py                 # Interfaz gráfica moderna
├── lexico.py              # Analizador léxico
├── sintactico.py          # Analizador sintáctico  
├── semantico.py           # Analizador semántico
├── simbolos.py            # Tabla de símbolos
├── intermedio.py          # Generador de código intermedio
└── traductor.py           # Traductor a otros lenguajes

#Ejemplo de codigo
int main() {
    int x = 10;
    float y = 3.14;
    
    if (x > 5) {
        printf("x es mayor que 5");
    }
    
    return 0;
}
#Ejecucion
python main.py
main.exe


# 🚀 Compilador con Interfaz Gráfica

Un compilador moderno desarrollado en Python con interfaz gráfica tkinter que realiza análisis léxico, sintáctico, semántico y generación de código intermedio.

 ✨ Características

- 🔤 Análisis Léxico**: Tokenización del código fuente
- 🌳 Análisis Sintáctico**: Construcción de árbol sintáctico
- 🔍 Análisis Semántico**: Verificación de tipos y errores
- 📚 Tabla de Símbolos**: Gestión de variables y funciones
- ⚡ Código Intermedio**: Generación de código de 3 direcciones
- 🌐 Traducción**: Conversión a Python, JavaScript y Java
- 🎨 Interfaz Gráfica**: Tema oscuro/claro intercambiable

🛠️ Tecnologías

- Python 3.x
- Tkinter (Interfaz gráfica)
- HTML (Documentación)

 🚀 Instalación y Uso

1. Clonar el repositorio:
   bash
   git clone https://github.com/EpickApollo/compilador.git
   cd compilador
