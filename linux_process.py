import logging
import psutil
from datetime import datetime

"""
logging.basicConfig(
    filename='reporte.log',       # Nombre del archivo
    level=logging.INFO,           # Nivel de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
"""

WHITELIST = [
	"systemd", "kthreadd", "pool_workqueue_release", "kworker/R-rcu_g", "kworker/R-slub_", "kworker/R-rcu_p", "kworker/R-netns", "kworker/0:0H-events_highpri", "kworker/R-mm_pe", "rcu_tasks_kthread", "rcu_tasks_rude_kthread", "rcu_tasks_trace_kthread", "ksoftirqd/0", "rcu_preempt",  "rcub/0", "migration/0", "idle_inject/0", "cpuhp/0", "cpuhp/1", "idle_inject/1", "migration/1", "ksoftirqd/1", "kworker/1:0H-events_highpri", "cpuhp/2", "idle_inject/2", "migration/2", "ksoftirqd/2", "kworker/2:0H-events_highpri", "cpuhp/3", "idle_inject/3", "migration/3", "ksoftirqd/3", "kworker/3:0H-events_highpri", "kdevtmpfs",  "kworker/R-inet_", "kauditd", "khungtaskd", "oom_reaper", "kworker/R-write", "kcompactd0", "ksmd", "khugepaged", "kworker/R-kinte", "kworker/R-blkcg", "kworker/R-tpm_d",
 "kworker/R-ata_s", "kworker/R-md", "kworker/R-md_bi",  "kworker/R-edac-",  "kworker/R-devfr",   "watchdogd",  "kworker/2:1H-events_highpri", "kswapd0",  "ecryptfs-kthread", "irq/122-aerdrv", "irq/122-pcie-dpc",   "kworker/R-acpi_",  "hwrng", "kworker/R-nvme-", "kworker/R-nvme-", "kworker/R-nvme-", "scsi_eh_0", "kworker/R-scsi_", "kworker/R-vfio-", "kworker/R-mld", "kworker/3:1H-events_highpri", "kworker/R-ipv6_", "kworker/R-kstrp",  "kworker/R-charg", "kworker/0:1H-events_highpri", "kworker/1:1H-events_highpri", 

"kworker/R-crypt",  "kworker/R-sdhci", "irq/130-0000:00:14.5 cd", "irq/53-ELAN1300:00", "irq/53-ELAN1300:00", "card0-crtc0", "card0-crtc1",  "card0-crtc2",  "spi1",  "jbd2/nvme0n1p4-8",  "kworker/R-ext4-",   "systemd-journald",  "systemd-udevd",  "psimon",   "jbd2/nvme0n1p2-8",  "kworker/R-ext4-",  "jbd2/nvme0n1p5-8",  "kworker/R-ext4-",  "kworker/R-cfg80", "irq/134-iwlwifi:default_queue", "irq/135-iwlwifi:queue_1", "irq/136-iwlwifi:queue_2", "irq/137-iwlwifi:queue_3", "irq/138-iwlwifi:queue_4", "irq/139-iwlwifi:exception",  "kworker/R-led_w",  "systemd-timesyncd", "accounts-daemon",  "acpid",  "avahi-daemon", "bluetoothd", "cron",  "dbus-daemon",  "avahi-daemon",  "fprintd",  "ll-package-manager", "ecbd",  "polkitd",  "snapd",  "smartd",  "systemd-logind",  "udisksd",  "NetworkManager", "deepin-service-manager",  "wpa_supplicant",  "ModemManager", "dde-dconfig-daemon", "dde-api-dbus-proxy-v1",  "containerd",  "lightdm", "sshd",  "Xorg",  "dde-system-daemon",  "uos-ste-resourced",  "upowerd",  "deepin-authentication",   "krfcommd",  "dockerd",  "nmbd",  "winbindd", "exim4", "wb[ALESSA-PC]",  "smbd", "smbd-notifyd", "smbd-cleanupd",  "lightdm", "wb-idmap", "systemd", "(sd-pam)", "ll-session-helper",  "pulseaudio",  "gnome-keyring-daemon",  "dbus-daemon",   "ibus-daemon", "dde-session", "gcr-ssh-agent", "gvfsd", "uos-ste-resourced", "startdde", "gvfsd-fuse", 

"psimon", "ibus-memconf", "ibus-ui-gtk3", "ibus-extension-gtk3", "ibus-x11", "at-spi-bus-launcher", "obexd", "dbus-daemon", "deepin-kwin_x11", "at-spi2-registryd", "xdg-desktop-portal",  "xdg-document-portal",  "xdg-permission-store",  "fusermount3",  "xdg-desktop-portal-gtk",  "ibus-engine-simple", "kglobalaccel5", "dconf-service", "dde-appearance", "dde-clipboard", "dde-file-manager-daemon", "dde-polkit-agent", "dde-session-daemon", "dde-application-manager", "dde-lock", "dde-shell", "dde-fakewm", "deepin-home-daemon",  

"agent", "deepin-ai-daemon", "gvfs-udisks2-volume-monitor", "gvfs-goa-volume-monitor",  "gvfs-gphoto2-volume-monitor",  "gvfs-mtp-volume-monitor", "gvfs-afc-volume-monitor",  "gvfsd-trash",  "dde-widgets",  "dde-clipboard-daemon", "gvfsd-metadata", "deepin-service-manager", "trayplugin-load","dde-api-dbus-proxy-v1",  "ll-cli", "ll-box",  "bash", "dde-calendar-service", "deepin-terminal", 

 "deepin-editor", "dde-file-manager", "deepin-home-appstore-client",  "deepin-home-appstore-daemon",   "gvfsd-network", "gvfsd-dnssd",  "cupsd",  "kworker/2:0-i915-unordered",  "kworker/0:0-events", "kworker/1:2-i915-unordered", "code", "kworker/u9:2+i915_flip", "kworker/u9:1-rb_allocator", "kworker/1:1-i915-unordered", "kworker/u8:13-events_unbound", "kworker/3:0-events", "kworker/2:2-inet_frag_wq", "kworker/0:3-events", "kworker/u8:6-events_power_efficient", "kworker/u8:10-flush-259:0", "kworker/u8:15-events_unbound", "irq/19-mmc0",   "irq/123-mei_me",  "kworker/u8:29-events_power_efficient",  "dde-osd",  "ipwatchd",   "kworker/0:1-events",   "kworker/2:1-cgroup_bpf_destroy","kworker/u9:0", "samba-dcerpcd", "rpcd_lsad", "rpcd_lsad",
 "deepin-sync-helper", "python", "kworker/2:0-events", "kworker/0:0-i915-unordered",  "kworker/u8:0+netns", "kworker/u8:3+events_unbound", "kworker/2:2+rcu_gp", "kworker/1:1-events", "kworker/3:2-events", "kworker/u8:2-flush-259:0", "kworker/R-kbloc", "kworker/3:1-events", "kworker/u8:4-flush-259:0",  "kworker/u9:0-rb_allocator", "kworker/1:2-mm_percpu_wq", "kworker/R-ttm", "kworker/2:3-events", "irq/133-mei_me", "kworker/u9:2-rb_allocator", "kworker/0:3-i915-unordered", "khidpd_054c0df4",
 "kworker/2:0-mm_percpu_wq", "kworker/u8:0-i915", "kworker/u8:3-events_unbound", "kworker/2:2-events", "kworker/3:2-events", "kworker/1:0-events", "kworker/u9:1+i915_flip",  "kworker/0:1-i915-unordered", "kworker/u8:1-events_unbound", "kworker/3:1-mm_percpu_wq", "kworker/u8:4-events_unbound", "kworker/u9:0+i915_flip", "kworker/1:1H-kblockd", "kworker/1:2-events", "kworker/u8:0-events_unbound", "kworker/u8:3-flush-259:0", "kworker/3:0", "kworker/u9:2-rb_allocator"


"docker-proxy", "containerd-shim-runc-v2", "mysqld", "docker-proxy", "mongod" #Procesos de docker

]

def mostrar_procesos_linux(whitelist, whitelist_pid=None):
    in_white = []
    not_in_white = []

    # Normalizar whitelist
    whitelist_normalized = set(p.lower().strip() for p in whitelist)
    whitelist_pid = whitelist_pid or [1]  # systemd

    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            nombre = proc.info['name']
            pid = proc.info['pid']
            if not nombre:
                continue

            nombre_normalizado = nombre.lower().strip()
            print(f"PID: {pid}, Nombre: {nombre_normalizado}")

            if pid in whitelist_pid or nombre_normalizado in whitelist_normalized:
                in_white.append(pid)
                print(f"✓ Proceso '{nombre}', PID: {pid} está en la whitelist")
            else:
                not_in_white.append(pid)
                print(f"✗ Proceso '{nombre}', PID: {pid} NO está en la whitelist")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return in_white, not_in_white

def end_process_linux(not_white):
    procesos_bloqueados = []

    for pid in not_white:
        try:
            p = psutil.Process(pid)
            user = p.username() 
            process_name = p.name()

            p.terminate()
            p.wait(timeout=5)

            procesos_bloqueados.append({
                "nombre": process_name,
                "pid": pid,
                "usuario": user,
                "hora": datetime.now().strftime("%H:%M:%S"),
                "motivo": "Proceso fuera de whitelist"
            })

            writing_log(f"✔ Proceso bloqueado: {process_name} (PID: {pid}), User: {user}", "info")

        except psutil.TimeoutExpired:
            try:
                p.kill()
            except:
                pass
        except (psutil.NoSuchProcess, psutil.AccessDenied, PermissionError) as e:
            print(f"✗ No se pudo terminar el proceso {pid}: {e}\n")

    return procesos_bloqueados


def writing_log(mensaje, nivel="info"):
    if nivel == "info":
        logging.info(mensaje)
    elif nivel == "warning":
        logging.warning(mensaje)
    elif nivel == "error":
        logging.error(mensaje)
    elif nivel == "debug":
        logging.debug(mensaje)
    elif nivel == "critical":
        logging.critical(mensaje)
    else:
        logging.info(mensaje)  


def main_linux():
    in_white, not_white = mostrar_procesos_linux(WHITELIST)
    print(f'Authorized Process = {len(in_white)}')
    print(f"Unathorized Process = {len(not_white)}")
    bloqueados = end_process_linux(not_white)
    return bloqueados