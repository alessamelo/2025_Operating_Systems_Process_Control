import tkinter as tk
from tkinter import messagebox
import datetime
import threading
import os
from main import set_timer, writing_log

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoreo de Prueba - Estudiante")

        self.nombre = ""
        self.cedula = ""
        self.email = ""

        # Teacher email
        tk.Label(root, text="Email:").grid(row=0, column=0, sticky='e')
        self.entry_email = tk.Entry(root)
        self.entry_email.grid(row=0, column=1)

        # Nombre
        tk.Label(root, text="Nombre completo:").grid(row=1, column=0, sticky='e')
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=1, column=1)

        # Cédula
        tk.Label(root, text="Cédula:").grid(row=2, column=0, sticky='e')
        self.entry_cedula = tk.Entry(root)
        self.entry_cedula.grid(row=2, column=1)

        # Hora inicio
        tk.Label(root, text="Hora inicio (HH:MM):").grid(row=3, column=0, sticky='e')
        self.entry_inicio = tk.Entry(root)
        self.entry_inicio.grid(row=3, column=1)

        # Hora fin
        tk.Label(root, text="Hora fin (HH:MM):").grid(row=4, column=0, sticky='e')
        self.entry_fin = tk.Entry(root)
        self.entry_fin.grid(row=4, column=1)

        # Botón iniciar
        self.boton_iniciar = tk.Button(root, text="Iniciar monitoreo", command=self.iniciar_monitoreo)
        self.boton_iniciar.grid(row=5, columnspan=2, pady=10)

        # Estado
        self.estado = tk.Label(root, text="🕒 Esperando...", fg="blue")
        self.estado.grid(row=6, columnspan=2)

        # Enlace al cerrar GUI
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def iniciar_monitoreo(self):
        self.nombre = self.entry_nombre.get().strip()
        self.cedula = self.entry_cedula.get().strip()
        self.email = self.entry_email.get().strip()
        hora_inicio = self.entry_inicio.get().strip()
        hora_fin = self.entry_fin.get().strip()

        if not self.nombre or not self.cedula or not hora_inicio or not hora_fin or not self.email:
            messagebox.showerror("Error", "Completa todos los campos")
            return

        try:
            t_inicio = datetime.datetime.strptime(hora_inicio, "%H:%M").time()
            t_fin = datetime.datetime.strptime(hora_fin, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Usa HH:MM")
            return

        writing_log(f"Estudiante: {self.nombre} - Cedula: {self.cedula} inicio monitoreo", "info")
        self.estado.config(text="🟡 En espera de inicio de monitoreo...", fg="orange")
        self.boton_iniciar.config(state="disabled")

        hilo = threading.Thread(target=self.ejecutar_timer, args=(t_inicio, t_fin))
        hilo.daemon = True
        hilo.start()

    def ejecutar_timer(self, t_inicio, t_fin):
        student_info = {
            "nombre": self.nombre,
            "cedula": self.cedula,
            "correo": self.email
        }
        set_timer(t_inicio, t_fin, student_info)
        self.estado.config(text="✅ Monitoreo finalizado", fg="green")
        writing_log(f"Estudiante: {self.nombre} - Cedula: {self.cedula} finalizo monitoreo", "info")

    def cerrar_aplicacion(self):
        self.root.destroy()
        os._exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

