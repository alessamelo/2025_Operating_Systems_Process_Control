import platform
import subprocess
import datetime

def mostrar_procesos_windows():
    try:
        salida = subprocess.check_output("tasklist", shell=True).decode("utf-8", errors="ignore")
        lineas = salida.strip().split('\n')
        print("📋 Procesos en ejecución (Windows):\n")
        for linea in lineas[3:]:  # saltamos los encabezados
            partes = linea.split()
            if len(partes) >= 2:
                nombre = partes[0]
                pid = partes[1]
                print(f"→ {nombre} (PID: {pid})")
    except Exception as e:
        print(f"⚠ Error al obtener procesos: {e}")

def mostrar_procesos_linux():
    try:
        salida = subprocess.check_output("ps -eo pid,comm", shell=True).decode("utf-8", errors="ignore")
        lineas = salida.strip().split('\n')
        print("📋 Procesos en ejecución (Linux/macOS):\n")
        for linea in lineas[1:]:
            partes = linea.strip().split(None, 1)
            if len(partes) == 2:
                pid, nombre = partes
                print(f"→ {nombre} (PID: {pid})")
    except Exception as e:
        print(f"⚠ Error al obtener procesos: {e}")

def main():
    so = platform.system().lower()
    if "windows" in so:
        mostrar_procesos_windows()
    elif "linux" in so or "darwin" in so:
        mostrar_procesos_linux()
    else:
        print("❌ Sistema operativo no soportado.")

if __name__== "__main__":
    main()