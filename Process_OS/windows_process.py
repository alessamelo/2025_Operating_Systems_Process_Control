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
    # Sistema base
    "System", "System Idle Process", "Registry", "MemCompression", "msedgewebview2.exe",
    "smss.exe", "csrss.exe", "wininit.exe", "services.exe", "lsass.exe",
    "svchost.exe", "fontdrvhost.exe", "dwm.exe",

    # Interfaz gráfica y shell
    "explorer.exe", "SearchApp.exe", "SearchIndexer.exe", "StartMenuExperienceHost.exe",
    "ShellExperienceHost.exe", "RuntimeBroker.exe", "sihost.exe", "ctfmon.exe",

    # Consolas y herramientas nativas
    "cmd.exe", "cmd64.exe", "conhost.exe", "powershell.exe", "powershell_ise.exe",
    "taskmgr.exe", "netstat.exe", "notepad.exe", "taskhostw.exe", "taskeng.exe",

    # Visual Studio Code y procesos de soporte
    "Code.exe", "CodeHelper.exe", "node.exe", "electron.exe", "WindowsTerminal.exe",
    "msbuild.exe", "python.exe", "python3.exe",

    # Herramientas de SysInternals u otras utilidades seguras
    "procexp.exe", "autoruns.exe", "procmon.exe",

    # Servicios de actualización, drivers o control
    "wuauclt.exe", "rundll32.exe", "audiodg.exe", "NisSrv.exe",
    "SecurityHealthService.exe", "SecurityHealthSystray.exe",
    "WMIPrvSE.exe", "TrustedInstaller.exe",

    # Drivers gráficos (opcional si usas Intel/Nvidia)
    "igfxtray.exe", "IntelGraphicsCommandCenter.exe", "igfxCUIService.exe", "igfxEM.exe",

    # Otros procesos permitidos (incluyendo específicos de Jade - HP)
    "ShellHost.exe", "AggregatorHost.exe", "WmiPrvSE.exe", "WUDFHost.exe", "LsaIso.exe",
    "unsecapp.exe", "MicUsage.exe", "RtkAudUService64.exe", "RtkAudioService64.exe",
    "NVDisplay.Container.exe", "uihost.exe", "wlanext.exe", "SearchProtocolHost.exe",
    "ipf_uf.exe", "ipfsvc.exe", "MsMpEng.exe", "MicrosoftEdgeUpdate.exe", "OfficeClickToRun.exe",
    "MpDefenderCoreService.exe", "spoolsv.exe", "KAPSService.exe", "KNDBWMService.exe",
    "KAPS.exe", "KNDBWM.exe", "AcerDIAgent.exe", "AcerCCAgent.exe", "UBTService.exe",
    "CamUsage.exe", "servicehost.exe", "ADESv2BW.exe", "Secure System", 
    "RtkNGUI64.exe", "EPCP.exe", "IntelCpHDCPSvc.exe", "LockApp.exe", "esif_uf.exe",
    "XtuService.exe", "IntelCpHeciSvc.exe", "LMS.exe", "jhi_service.exe", "dllhost.exe",
    "smartscreen.exe", "PresentationFontCache.exe", "AppVShNotify.exe", "UserOOBEBroker.exe",
    "CompPkgSrv.exe", "EEventManager.exe", "ETDTouch.exe", "SystemSettingsBroker.exe",
    "ApplicationFrameHost.exe", "esif_assist_64.exe", "PhoneExperienceHost.exe", "ETDCtrl.exe",
    "TextInputHost.exe", "RAVBg64.exe", "aesm_service.exe", "SocketHeciServer.exe",
    "ETDCtrlHelper.exe", "Microsoft.SharePoint.exe", "logi_crashpad_handler.exe",
    "FileCoAuth.exe", "identity_helper.exe", "SearchHost.exe", "TabTip.exe",

    #Dell = Windows
    "lsass.exe", "fontdrvhost.exe", "WUDFHost.exe", "IntelCpHDCPSvc.exe", "NVDisplay.Container.exe", "wsc_proxy.exe", "Memory",
    "igfxCUIServiceN.exe", "aswToolsSvc.exe", "spoolsv.exe", "WmiPrvSE.exe", "aswEngSrv.exe", "PresentationFontCache.exe",
    "dasHost.exe", "aswidsagent.exe", "SearchIndexer.exe", "unsecapp.exe", "afwServ.exe", "AdminService.exe", "OneApp.IGCC.WinService.exe",
    "armsvc.exe", "svchost.exe", "OfficeClickToRun.exe", "esif_uf.exe", "nvcontainer.exe", "jhi_service.exe", "QcomWlanSrvx64.exe",
    "SmartByteAnalyticsService.exe", "servicehost.exe", "RtkAudUService64.exe", "SmartByteNetworkService.exe", "RstMwService.exe",
    "MpDefenderCoreService.exe", "WavesSysSvc64.exe", "WMIRegistrationService.exe", "MsMpEng.exe", "escsvc64.exe", "RAPSService.exe",
    "RAPS.exe", "conhost.exe", "AggregatorHost.exe", "SecurityHealthService.exe", "Dell.D3.WinSvc.exe", "DellSupportAssistRemedati.exe",
    "ServiceShell.exe", "csrss.exe", "winlogon.exe", "dwm.exe", "uihost.exe", "sihost.exe", "igfxEMN.exe", "taskhostw.exe", "ShellHost.exe",
    "explorer.exe", "SearchHost.exe", "StartMenuExperienceHost.exe", "RuntimeBroker.exe", "Widgets.exe", "WidgetService.exe",
    "smartscreen.exe", "ctfmon.exe", "SecurityHealthSystray.exe", "ShellExperienceHost.exe", "SearchFilterHost.exe",
    "SearchProtocolHost.exe", "dllhost.exe", "ApplicationFrameHost.exe", "audiodg.exe", "WindowsPackageManagerServ.exe", "VSSVC.exe",
    "SrTasks.exe", "msiexec.exe", "UserOOBEBroker.exe", "Code.exe", "pet.exe", "cmd.exe", "tasklist.exe", "AvastUI.exe", 


    #Lenovo = Windows
    "ETDService.exe", "spoolsv.exe", "OfficeClickToRun.exe", "MpDefenderCoreService.exe", "MsMpEng.exe", "RtkAudUService64.exe", "DAX3API.exe", "FMService64.exe", "RtkBtManServ.exe",
    "dasHost.exe", "DAX3API.exe", "audiodg.exe",  "dllhost.exe", "ETDCtrlHelper.exe", "ETDCtrl.exe",  "sihost.exe", "taskhostw.exe", "explorer.exe",  "ETDTouch.exe",  "SearchIndexer.exe", 
    "StartMenuExperienceHost.exe", "RuntimeBroker.exe", "SearchApp.exe", "ctfmon.exe", "NisSrv.exe", "TextInputHost.exe", "SecurityHealthSystray.exe",
    "SecurityHealthService.exe", "RtkAudUService64.exe", "taskhostw.exe", "conhost.exe", "cmd.exe",  "ApplicationFrameHost.exe", "UserOOBEBroker.exe",  "SgrmBroker.exe", "CompPkgSrv.exe",
    "WmiPrvSE.exe", "SearchProtocolHost.exe","OfficeClickToRun.exe", "HxOutlook.exe", "HxTsr.exe", "HxAccounts.exe", "MicrosoftEdgeUpdate.exe", "tasklist.exe",
    "ShellExperienceHost.exe", "SystemSettings.exe", "backgroundTaskHost.exe"
]


WHITELIST_PID = [0, 4, 428]

def mostrar_procesos_windows(whitelist, whitelist_pid):
    in_white = []
    not_in_white = []

    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            nombre = proc.info['name']
            pid = proc.info['pid']
            print(f"PID: {pid}, Nombre: {repr(nombre)}")

            if pid in whitelist_pid or (nombre and nombre in whitelist):
                in_white.append(pid)
                print(f"✓ Proceso '{nombre}', '{pid}' está en la whitelist")
            else:
                not_in_white.append(pid)
                print(f"✗ Proceso '{nombre}', '{pid}' NO está en la whitelist")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return in_white, not_in_white 



def end_process_windows(not_white):
    procesos_bloqueados = []

    for pid in not_white:
        try:
            p = psutil.Process(pid)
            user = p.username() 
            process_name = p.name()

            p.terminate()
            p.wait(timeout=5)

            # Si terminó correctamente, lo agregamos a la lista
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
                p.terminate()
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


def main_windows():
    in_white, not_white = mostrar_procesos_windows(WHITELIST, WHITELIST_PID)
    print(f'Authorized Process = {len(in_white)}')
    print(f"Unathorized Process = {len(not_white)}")
    bloqueados = end_process_windows(not_white)
    return bloqueados


