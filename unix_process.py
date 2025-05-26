import logging
import psutil
import os
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
	    "launchd",   "logd",   "smd",   "UserEventAgent",   "fseventsd",   "mediaremoted",   "systemstats",   "accessoryupdaterd",  "configd",   "endpointsecurityd",   "powerd",  "IOMFB_bics_daemon",   "amfid",   "keybagd",   "softwareupdated",   "corespeechd_system", 
        "UserEventAgent",  "fseventsd",  "mediaremoted",  "systemstats",  "accessoryupdaterd",  "configd",  "endpointsecurityd",  "powerd",  "IOMFB_bics_daemon",  "amfid",  "keybagd",  "softwareupdated",  "corespeechd_system",  "watchdogd",  "mds",
        "iconservicesd",  "kernelmanagerd",  "diskarbitrationd",  "coreduetd",  "syslogd",  "thermalmonitord",  "opendirectoryd",  "apsd",  "launchservicesd",  "timed",  "usbmuxd",  "securityd",  "locationd",  "nesessionmanager",  "autofsd",
        "dasd",  "distnoted",  "AppleCredentialManagerDaemon",  "dirhelper",  "logind",  "revisiond",  "KernelEventAgent",  "usermanagerd",  "notifyd",  "sandboxd",  "corebrightnessd",  "AirPlayXPCHelper",   "com.apple.cmio.registerassistantservice",
        "aslmanager",  "logd_helper",  "WindowServer",  "tccd",  "cfprefsd",  "loginwindow",  "runningboardd",  "contextstored",  "coreservicesd",  "containermanagerd_system",  "airportd",  "systemstatusd",  "trustd",  "coreaudiod",  "liquiddetectiond",  
        "com.apple.ifdreader",  "apfsd",  "nsurlsessiond",  "lsd",  "nehelper",  "usbd",  "analyticsd",   "biometrickitd",  "eligibilityd",  "hidd",  "secinitd",  "trustdFileHelper",  "powerexperienced",  "distnoted",  "backupd-helper",  "PowerUIAgent",  
        "csnameddatad",  "mobileassetd",  "com.apple.audio.DriverHelper",  "authd",  "cryptexd",  "AudioComponentRegistrar",  "syspolicyd",  "storagekitd",  "mDNSResponder",  "com.apple.audio.SandboxHelper",  "biomed",  "audioclocksyncd",   "colorsync.displayservices",  
        "com.apple.ColorSyncXPCAgent",  "colorsyncd",   "com.apple.CodeSigningHelper",   "socketfilterfw",   "com.apple.DriverKit-AppleBCMWLAN",    "com.apple.DriverKit-IOUserDockChannelSerial", "appleeventsd",   "com.apple.AppleUserHIDDrivers",  "audioanalyticsd", 
        "AppleDeviceQueryService",  "sysextd",  "aneuserd",  "aned",  "symptomsd",  "modelmanagerd",  "ViewBridgeAuxiliary",  "bootinstalld",  "mDNSResponderHelper",  "PlugInLibraryService",  "modelcatalogd",  "backgroundtaskmanagementd",  "softwareupdated",  
        "PerfPowerTelemetryClientRegistrationService",  "XProtectPluginService",  "symptomsd-diag",  "backupd",  "rtcreportingd",  "securityd_system",  "suhelperd", "com.apple.hiservices-xpcservice",  "appleh13camerad",  "cameracaptured",  "online-auth-agent",  
        "uvcassistant",  "wirelessradiomanagerd",  "findmybeaconingd",  "com.apple.geod",  "distnoted",  "gsscred",  "mds_stores",  "secinitd",  "cfprefsd",  "trustd",  "containermanagerd",  "searchpartyd",  "coreauthd",  "applekeystored",  "corekdld",  
        "usereventagent",  "gamecontrollerd",  "seld",  "neagent",  "coreservicesuiagent",  "universalaccessd",  "pboard",  "windowmanager",  "talagentd",  "findmydeviced",  "dock",  "controlcenter",  "watchdogd",   "launchd",   "logd",  "smd",   "systemuiserver",
        "finder",  "lsd",  "com.apple.geod",  "knowledge-agent",  "csnameddatad",  "secd",  "secinitd",  "dmd",  "quicklookuiservice",  "bird",  "findmydevice-user-agent",  "com.apple.quicklook.thumbnailsagent",  "trustd",  "mobileactivationd",  "wallpaperagent",  
        "filecoordinationd",  "distnoted",  "siriactionsd",  "automountd",  "com.apple.hiservices-xpcservice",  "sharedfilelistd",  "containermanagerd",  "usernotificationsd",  "corelocationagent",   "suggestd",  "tccd",  "sociallayerd",  "callservicesd",  "calaccessd", 
        "iconservicesagent",  "fileproviderd",  "pkd",  "ampdevicediscoveryagent",  "identityservicesd",  "viewbridgeauxiliary",  "intelligentroutingd",  "donotdisturbd",  "rapportd",  "mobiletimerd",  "replayd",  "audiocomponentregistrar",  "wallpaperexportd",  
        "extensionkitservice",  "fontd",  "wallpaperimageextension",  "triald",  "accountsd",   "carboncomponentscannerxpc",  "oahd",  "fontworker",  "findmylocateagent",  "cloudd",  "cfprefsd",  "ctkd",  "transparencyd",  "syncdefaultsd",  "bluetoothuserd",  "coreauthd",
        "trustd",  "usernoted",  "useractivityd",  "com.apple.dock.extra",  "ndoagent",  "commcenter",  "icloudmailagent",  "containermanagerd",  "notificationcenter",  "distnoted",  "familycircled",  "statuskitagent",  "akd",  "sharingd",  "replicatord",  "nsurlsessiond",  
        "generativeexperiencesd",  "deleted",   "callhistorypluginhelper",  "awdd",  "screentimeagent",  "managedsettingsagent",  "chronod",  "routined",  "lockoutagent",  "appleaccountd",  "apfsuseragent",  "reportcrash",  "biomeagent",  "continuitycaptureagent",  
        "assistantd",  "wifip2pd",  "wifiagent",  "loginuserservice",  "followupd",  "nearbyd",  "mtlassetupgrderd",  "networkserviceproxy",  "swcd",  "duetexpertd",  "com.apple.geod",  "linkd",  "menotificationagent",  "backgroundtaskmanagementagent",  "siriknowledged",
        "homed",  "cloudd",  "localizationswitcherd",  "extensionkitservice",  "imagent",  "appssoagent",  "wificloudassetsxpcservice",  "familycontrolsagent",  "com.apple.facetime.ftconversationservice",  "cdpd",  "appssodaemon",  "trustedpeershelper",  "imdpersistenceagent", 
        "corespeechd",  "axassetsd",  "contextstoreagent",  "imklaunchagent",  "icdd",  "askpermissiond", "airplayuiagent",  "diagnostics_agent",  "textinputmenuagent",  "amsaccountsd",  "ctkahp",  "mediaremoteagent",  "wificloudassetsxpcservice",  "csexattrcryptoservice", 
        "spotlight",  "avconferenced",  "textinputswitcher",  "cursoruiviewservice",  "pbs",  "extensionkitservice",  "corespotlightd",  "containermetadataextractor",  "parsecd",  "pah_extension",  "com.apple.clouddocs.iclouddrivefileprovider", "stockswidget",
        "localspeechrecognition",  "itunescloudd",  "amsengagementd",  "sirittsd",  "assistant_cdmd",  "screentimewidgetextension",  "contactsdonationagent",  "swtransparencyd",  "findmywidgetpeople",  "icloudnotificationagent",  "corethreadcommissionerserviced",  "adid", 
        "voicememossettingswidgetextension",  "contextservice",  "uarpupdaterservicedisplay",  "uarpupdaterserviceafu",  "uarpupdaterservicehid",  "mobiledeviceupdater",  "distnoted",   "UARPUpdaterServiceDFU",   "UARPUpdaterServiceUSBPD",  "UARPUpdaterServiceLegacyAudio", 
        "PhotosReliveWidget",  "MDRemoteServiceSupport",  "systemsoundserverd",  "CloudTelemetryService",  "ProtectedCloudKeySyncing",  "wifianalyticsd",  "Keychain Circle Notification",  "seserviced",  "AssetCacheLocatorService",  "AssetCache",  "CalendarWidgetExtension",  
        "sysmond",  "WorldClockWidget",  "osanalyticshelper",  "UIKitSystem",  "IntentsExtension", "photolibraryd",  "spindump",  "scopedbookmarkagent",  "spindump_agent",  "submitdiaginfo",  "homewidget",  "mobiletimerintents",  "weatherintents",  "commerce",  
        "coresymbolicationd",  "tipswidgetextension",  "peoplewidget_macosextension",  "podcastswidget",  "batteriesavocadowidgetextension",  "findmywidgetitems",  "selectperson_ios",  "mtlcompilerservice",  "reminderswidgetextension", "safariwidgetextension",
        "shortcutswidgetextension",  "com.apple.notes.widgetextension",  "homeenergywidgetsextension",  "remindersintentsextension",  "com.apple.notes.intentsextension",  "categoriesservice",  "financed",  "screentimewidgetintentsextension",  "cloudtelemetryservice",  
        "com.apple.sbd",  "mediaanalysisd",  "photoanalysisd",  "assetcachetetheratorservice",  "callhistorysynchelper",  "xprotectbridgeservice",  "nfcd", "NFStorageServer",    "distnoted",    "ModelCatalogAgent",    "countryd",    "systemstats",    "SetStoreUpdateService",    
        "gamecontrolleragentd",    "mdbulkimport",    "captiveagent",    "SoftwareUpdateNotificationManager",    "UsageTrackingAgent",    "deleted_helper",    "XProtectPluginService",    "com.apple.MobileSoftwareUpdate.CleanupPreparePathService",    "XprotectService",    
        "ReportCrash",    "OSDUIHelper",     "maild",    "diagnosticextensionsd",    "lockdownmoded",    "siriinferenced",    "CMFSyncAgent",    "colorsync.useragent",    "progressd",    "milod",    "gamepolicyd",    "geodMachServiceBridge",    "installd",    "system_installd",    
        "appstoreagent",    "installcoordinationd",    "com.apple.AppStoreDaemon.StorePrivilegedODRService",    "fairplayd",    "installerauthagent",    "NRDUpdated",   "analyticsagent",     "mapssyncd",    "akd",    "AssetCacheLocatorService",    "promotedcontentd",  
        "fairplaydeviceidentityd",    "ThunderboltAccessoryUpdaterService",    "MTLCompilerService",    "com.apple.StreamingUnzipService.privileged",    "com.apple.NRD.UpdateBrainService",    "xpcroleaccountd",    "spotlightknowledged",    "nsattributedstringagent",   
        "com.apple.hiservices-xpcservice",    "FindMyDeviceIdentityXPCService",    "cfprefsd",    "weatherd",    "com.apple.accessibility.mediaaccessibilityd", "com.apple.accessibility.mediaaccessibilityd",    "extensionkitservice",    "CalendarIntentsExtension",    
        "com.apple.audio.ComponentTagHelper",    "triald_system",    "com.apple.audio.SandboxHelper",    "AUCrashHandlerService",    "WardaSynthesizer_x86_64",    "WardaSynthesizer_arm64", "GMSSELFIngestor", "IFTranscriptSELFIngestor", "IFTelemetrySELFIngestor", "MacinTalkAUSP",
        "KonaSynthesizer", "CrashReporterSupportHelper", "com.apple.audio.SandboxHelper", "managedcorespotlightd", "extensionkitservice", "adprivacyd",    "distnoted",    "mdbulkimport",    "cfprefsd",    "pkd",    "dataaccessd",    "lsd",    "csnameddatad",    "secd",    
        "containermanagerd",    "mdworker",    "trustd",    "peopled",    "contactsd",    "spotlightknowledged",    "fudHelperAgent",    "powerdatad",    "remotemanagementd", "PasswordBreachAgent", "geoanalyticsd", "inputanalyticsd", "PasswordBreachAgent", "coreautha",
        "passd",    "USBAgent",    "XProtect",    "PowerChime",    "com.apple.geod",     "MTLCompilerService",    "audiomxd",    "secinitd",    "cfprefsd",    "trustd",  "containermanagerd", "metrickitd", "XProtect", "keychainsharingmessagingd",  "ciphermld",  "cfprefsd", 
        "extensionkitservice",  "mmaintenanced", "nbagent", "nbstated",    "dprivacyd", "dprivacyd", "RemoteManagementAgent", "SecuritySubscriber", "InteractiveLegacyProfilesSubscriber", "ScreenSharingSubscriber", "LegacyProfilesSubscriber", "PasscodeSettingsSubscriber",
        "AccountSubscriber", "ManagementTestSubscriber", "ASConfigurationSubscriber", "ManagedSettingsSubscriber", "microstackshot", "AMPLibraryAgent", "AMPArtworkAgent", "iconservicesagent", "MTLCompilerService","distnoted", "cfprefsd", "sysdiagnosed",    "loginwindow",    
        "UserEventAgent",    "mobiletimerd", "replicatord", "generativeexperiencesd",     "CoreServicesUIAgent",    "universalaccessd", "pboard", "usernotificationsd", "accountsd", "identityservicesd", "nsurlsessiond", "callservicesd","CommCenter", "rapportd", "mediaanalysisd", 
        "geoanalyticsd", "routined","APFSUserAgent", "usernoted","talagentd", "WindowManager",    "secinitd","lockoutagent", "triald", "ContextStoreAgent", "ndoagent", "CoreLocationAgent",   "geod","dmd", "BiomeAgent",   "ScreenTimeAgent",    "tccd", "neagent", "syncdefaultsd",  
        "networkserviceproxy",  "homed",  "chronod", "corespotlightd",  "swcd",  "duetexpertd", "amsondevicestoraged",  "linkd",  "findmylocateagent",  "ctkd",    "transparencyd",    "coreauthd",    "sharingd", "fileproviderd",  "ManagedSettingsAgent",  "followupd",    "deleted",    
        "StatusKitAgent",    "sharedfilelistd",   "FamilyControlsAgent",    "familycircled",    "MTLAssetUpgraderD",    "MENotificationAgent",    "BackgroundTaskManagementAgent",    "appleaccountd",    "localizationswitcherd",    "cdpd",   "akd",  "extensionkitservice",    
        "CMFSyncAgent",    "iconservicesagent",    "ViewBridgeAuxiliary",    "UIKitSystem",    "intents_helper",    "milod",    "IMDPersistenceAgent",    "ContainerMetadataExtractor",   "ContinuityCaptureAgent", "suggestd", "ProtectedCloudKeySyncing",    "Keychain Circle Notification",
        "seserviced",   "fontd",    "fontworker",    "photolibraryd",    "BTLEServerAgent",    "analyticsagent",    "ScopedBookmarkAgent",    "UniversalControl",    "SidecarRelay",    "Dock",    "ControlCenter",    "SystemUIServer",    "Finder",    "com.apple.ColorSyncXPCAgent",   
        "WallpaperAgent",    "calaccessd",    "imklaunchagent",    "com.apple.quicklook.ThumbnailsAgent",    "QuickLookUIService",    "AMPDeviceDiscoveryAgent",    "PAH_Extension",    "pbs",    "com.apple.CloudDocs.iCloudDriveFileProvider",    "extensionkitservice",    "WallpaperImageExtension",    
        "PlugInLibraryService",    "intelligentroutingd",    "replayd",    "AudioComponentRegistrar",    "CarbonComponentScannerXPC",    "com.apple.dock.extra" 
]

def mostrar_procesos_unix(whitelist, whitelist_pid=None):
    in_white = []
    not_in_white = []

    whitelist_normalized = set(os.path.basename(p).lower().strip() for p in whitelist)
    whitelist_pid = whitelist_pid or [1]  # por defecto permitir PID 1 (ej. launchd o systemd)

    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            pid = proc.info['pid']
            nombre = proc.info['name']
            if not nombre:
                continue

            # Extraer solo el nombre base del ejecutable
            nombre_base = os.path.basename(nombre).lower().strip()

            print(f"PID: {pid}, Nombre: {nombre_base}")

            if pid in whitelist_pid or nombre_base in whitelist_normalized:
                in_white.append(pid)
                print(f"✓ Proceso '{nombre_base}', PID: {pid} está en la whitelist")
            else:
                not_in_white.append(pid)
                print(f"✗ Proceso '{nombre_base}', PID: {pid} NO está en la whitelist")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return in_white, not_in_white

def end_process_unix(not_white):
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
                "hora": datetime.datetime.now().strftime("%H:%M:%S"),
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


def main_unix():
    in_white, not_white = mostrar_procesos_unix(WHITELIST)
    print(f'Authorized Process = {len(in_white)}')
    print(f"Unathorized Process = {len(not_white)}")
    bloqueados = end_process_unix(not_white)
    return bloqueados



