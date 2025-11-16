import os
import subprocess
import sys

def compilar_app():
    # Verificar que main.py existe
    if not os.path.exists("main.py"):
        print("❌ ERROR: No se encuentra main.py en el directorio actual")
        print("Directorio actual:", os.getcwd())
        return
    
    print("✅ main.py encontrado")
    print("🔨 Compilando aplicación...")
    
    # Comando de PyInstaller
    comando = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=CompiladorApp",
        "main.py"
    ]
    
    try:
        subprocess.run(comando, check=True)
        print("✅ ¡Compilación exitosa!")
        print("📁 El ejecutable está en: dist/CompiladorApp.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la compilación: {e}")
    except FileNotFoundError:
        print("❌ PyInstaller no está instalado")
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        # Intentar nuevamente
        subprocess.run(comando, check=True)

if __name__ == "__main__":
    compilar_app()