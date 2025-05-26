# 2025_Operating_Systems_Process_Control
This project is focused on the development of a process monitoring system designed to ensure exam integrity by controlling the execution of system processes during an exam session. The application allows instructors to define a whitelist of authorized processes, while automatically detecting, blocking, and terminating any non-authorized applications that might indicate academic dishonesty.

Built using Python, the system includes a lightweight graphical interface and leverages real-time process tracking to monitor student activity. The instructor can remotely initiate and terminate monitoring sessions, log user identity for traceability, and receive alerts about violations. The goal is to offer a portable, easy-to-use solution that works across different machines, without requiring deep technical knowledge from users.

This project integrates system-level control, user authentication, and GUI/API design, offering a practical tool for maintaining a secure digital exam environment.

# 🖥️ Process Monitoring System – Anti-Cheat Tool for Exams

This project implements a system to **monitor and block unauthorized processes** during digital exams using Python, `psutil`, `Tkinter`, and a configurable OS-specific whitelist.

## 🚀 Features

- ✅ **Cross-platform:** Compatible with Windows, Linux, and macOS.
- 🔐 **Educational focus:** Ideal for preventing cheating during supervised assessments.
- 🧠 **Graphical Interface (Tkinter):** Easy-to-use UI for instructors or supervisors.
- 📋 **JSON and LOG reports:** Detailed evidence of any unauthorized activity.
- ⚙️ **Modular & Extensible:** Clean architecture with OS-separated logic (`Process_OS/`).

---

## 🗂️ Project Structure

project-root/
            │
            ├── gui.py # Graphical interface (Tkinter)
            ├── main.py # Main logic triggered by GUI
            │
            ├── Process_OS/
            │ ├── windows_process.py # Windows-specific logic
            │ ├── linux_process.py # Linux-specific logic
            │ └── unix_process.py # macOS-specific logic
            │
            ├── reporte.log # Plain text log (auditing)
            ├── reporte.json # Structured report with student info
            └── README.md # (This file)


## 🧰 Requirements

psutil
datetime
os
logging


## ▶️ How to Use
Run the graphical interface:
python gui.py
Enter student details: name, ID, and email.

Click "Start Monitoring" to begin the exam monitoring session.

The system will:

-Automatically detect the host OS.

-Load the appropriate script from Process_OS/.

-Identify active processes.

-Compare against the whitelist.

-Block unapproved processes.

-Log violations in reporte.log and reporte.json.

When "Stop" is clicked, monitoring ends and reports are generated.

##🧾 Generated Reports
reporte.log: Plain text log with timestamp, process name, PID, and termination reason.

reporte.json: Includes student information and a list of blocked processes in JSON format.

##📌 Considerations
-⚠️ In case you want to increment the whitelist process, configure the whitelist properly to avoid terminating essential system processes.

-✅ You can edit the WHITELIST in each *_process.py file.

-💻 Ideal for university labs, supervised classrooms, or virtual assessments.


##❗ Limitations
Some orphaned or unnamed processes might not be verifiable. The current whitelist is based on testing across 10 different laptops and OS configurations.
Ensure that critical system processes are never terminated.


📝 License
This project is for educational use. You are free to modify and adapt it for academic purposes.
