import platform
import time
import datetime
import json
import os
import logging
from Process_OS.windows_process import main_windows, writing_log
from Process_OS.linux_process import main_linux
from Process_OS.unix_process import main_unix


def set_timer(init, endt, student_info=None):
    os_type = platform.system().lower()

    if student_info:
        configurar_log(student_info)  # 👈 Esto va aquí

    procesos_bloqueados = []

    now = datetime.datetime.now()
    start_time = datetime.datetime.combine(now.date(), init)
    end_time = datetime.datetime.combine(now.date(), endt)
    if end_time <= start_time:
        end_time += datetime.timedelta(days=1)

    writing_log("\n****************************** Start Report *******************************\n", "info")
    print(f"🟢 Esperando hasta {start_time.time()} para iniciar el monitoreo...")

    while datetime.datetime.now() < start_time:
        time.sleep(1)

    print(f"🚨 Monitoreo activo hasta las {end_time.time()}...\n")

    while datetime.datetime.now() < end_time:
        if os_type == "windows":
            procesos_bloqueados += main_windows()
        elif os_type == "linux":
            procesos_bloqueados += main_linux()
        elif os_type == "darwin":
            procesos_bloqueados += main_unix()
        time.sleep(1)

    print("✅ Monitoreo finalizado.")

    if student_info:
        guardar_reporte_json(student_info, init, endt, procesos_bloqueados)

    writing_log("\n****************************** End Report *******************************\n", "info")


def guardar_reporte_json(info, inicio, fin, procesos):
    nombre_archivo = f"{info['cedula']}_{info['nombre'].replace(' ', '_')}.json"

    data = {
        "nombre": info["nombre"],
        "cedula": info["cedula"],
        "correo": info.get("correo", ""),
        "fecha": str(datetime.date.today()),
        "hora_inicio": str(inicio),
        "hora_fin": str(fin),
        "procesos_bloqueados": procesos
    }

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"📄 Reporte guardado como {nombre_archivo}")

def configurar_log(student_info):
    log_file = f"{student_info['cedula']}_{student_info['nombre'].replace(' ', '_')}.log"

    # Reset logging handlers si ya había uno
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    init = datetime.datetime.strptime(input("Start Time (HH:MM): "), "%H:%M").time()
    endt = datetime.datetime.strptime(input("End Time (HH:MM): "), "%H:%M").time()

    writing_log("\n****************************** Report *******************************\n", "info")

    # Para pruebas sin GUI (sin datos del estudiante)
    set_timer(init, endt)

    writing_log("\n****************************** End Report *******************************\n", "info")


if __name__ == "__main__":
    main()

