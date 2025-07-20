import os
import subprocess
import sys
from pathlib import Path

def create_virtualenv():
    """Crea el entorno virtual si no existe"""
    if not Path("venv").exists():
        print("[+] Creando entorno virtual...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("[✓] Entorno virtual creado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"[x] Error creando entorno virtual: {e}")
            sys.exit(1)
    else:
        print("[*] Entorno virtual ya existe.")

def install_requirements():
    """Instala las dependencias desde requirements.txt"""
    pip_path = Path("venv") / "Scripts" / "pip.exe"
    requirements_file = Path("requirements.txt")
    
    if not pip_path.exists():
        print("[x] pip no encontrado. ¿Se creó correctamente el entorno virtual?")
        sys.exit(1)
    
    if not requirements_file.exists():
        print("[!] Advertencia: requirements.txt no encontrado. Saltando instalación de dependencias.")
        return
    
    print("[+] Instalando dependencias...")
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("[✓] Dependencias instaladas exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"[x] Error instalando dependencias: {e}")
        sys.exit(1)

def run_program():
    """Ejecuta el programa principal"""
    python_path = Path("venv") / "Scripts" / "python.exe"
    program_file = Path("main2_changue_draw.py")
    
    if not python_path.exists():
        print("[x] Python no encontrado en el entorno virtual.")
        sys.exit(1)
    
    if not program_file.exists():
        print("[x] Archivo main2_changue_draw.py no encontrado.")
        sys.exit(1)
    
    print("[+] Ejecutando programa...")
    try:
        subprocess.run([str(python_path), "main2_changue_draw.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[x] Error ejecutando el programa: {e}")
    except KeyboardInterrupt:
        print("\n[*] Programa interrumpido por el usuario.")

def main():
    """Función principal que ejecuta todo el proceso"""
    print("=== Automatización: Cronograma 28 de Julio (Windows) ===\n")
    
    try:
        create_virtualenv()
        install_requirements()
        run_program()
    except Exception as e:
        print(f"[x] Error inesperado: {e}")
        sys.exit(1)
    
    print("\n[✓] Proceso completado.")

if __name__ == "__main__":
    main()
