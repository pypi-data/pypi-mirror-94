import os

import m360


class Settings:

    #SOBREESCRIBE EL HOSTNAME DE LA MAQUINA
    HOSTNAME = ""

    '''PATH ABSOLUTO DE LOS COLECTORES'''
    MONITOR_PATH = os.path.dirname(os.path.dirname(__file__)) #apunta a la carpeta src
    ##TODO: SI ES WINDOWS, POR DEFECTO EN C:/M360/telegraf/data
    BASE_DIR = os.path.dirname(MONITOR_PATH)

    PIDFILE = os.path.join(MONITOR_PATH,"ptelegraf.pid")

    ##TODO: SI ES WINDOWS, POR DEFECTO EN C:/M360/telegraf/logs
    LOG_DIR = os.sep+os.path.join("var","log","telegraf")
    GRAFANA_HOME=os.path.dirname(BASE_DIR) #apunta a la carpeta de la instalacion

    ''' DIRECTORIO DE ARCHIVOS DE CACHE, TEMPORALES, INDICES, ETC..'''
    MONITOR_CACHE=os.path.join(BASE_DIR,'cache')
    if not os.path.isdir(MONITOR_CACHE):
        try:
            os.makedirs(MONITOR_CACHE, 0o775)
        except Exception as e:
            pass

    '''AUTODETECCION EN LA MEDIDA POSIBLE DE LAS INSTANCIAS A MONITORIZAR'''
    AUTODETECT = True
    DEBUG = False
    DEBUG_HPUX=True
    ENABLED = True

    '''DIAS EN EL PASADO QUE BUSCAMOS LOGS POR SI NO SE HAN RECOLECTADO'''
    RETENTION = 2

    '''PARA CREAR IDENTIFICADORES UNICOS'''
    SEED = '97h!$ido=4&%_7*wj4=7l!st)-0lpg#od5t(sdi)4#exgijpn6'

    '''MONITORES PERMITIDOS, SOLO ESTOS SE PUEDEN LANZAR SI ADEMAS EXISTE SU FICHERO
    CORRESPONDIENTE EN conf/<colector>.py'''

#Configured by install
    ALLOWED_TECHNOLOGY = ["tomcat","oraclecloud","jboss","weblogic","oracle"]
    TECHNOLOGY_HEALTH = ["oracle","tomcat","oraclecloud","jboss","weblogic","apache","unix","windows"]
    TECHNOLOGY_WITH_VERSION = TECHNOLOGY_HEALTH + ["internal"]
    '''ZONA HORARIA DEL SERVIDOR PAR DIFERENCIAR DE LOS TIMESTAMPS REMOTOS
    QUE PUEDEN ESTAR EN OTRO TIMEZONE'''
    TIME_ZONE = 'Europe/Madrid'

    GLOBAL_PATTERNS = os.path.join(MONITOR_PATH, 'patterns')

    LOGFORMAT = '[%(asctime)-15s] [%(levelname)s] [%(threadName)s] [%(name)s] [%(monitor)s] [%(modulo)s] %(message)s'
    LOGFORMAT_DEBUG = '[%(asctime)-15s] [%(levelname)s] [%(threadName)s] [%(name)s] [%(filename)s] [%(funcName)s] %(message)s'

    METRICLOGFORMAT = "{timestamp} {host} {date} {time} {tech} \"{version}\" {instance} {metrics}"
    #s,ms,ns,us
    PRECISION="us"

    AUTONOMOUS = "oci_autonomous_database"
    ACCESS = "access"
    HEAP = "heap"
    MODULE = "module"
    THREADS = "threads"
    HTTP = "http"
    POOL = "pool"
    GC = "gc"
    JMS = "jms"
    PSMON = "psmon"
    RCMON = "rcmon"
    PROCSTAT = "procstat"
    PROCSTAT_LOOKUP = "lookup"
    WEBAPPLMON = "webapplmon"
    CPU = "cpu"
    TOP = "top"
    NSTAT = "nstat"
    NETSTAT = "netstat"
    PROCESSES = "processes"
    NETWORK = "net"
    LOAD = "load"
    MEMORY = "mem"
    SWAP = "swap"
    DISK = "disk"
    ESL = "esl"
    DISKIO = "diskio"
    SYSTEM = "system"
    APP = "app"
    HEALTH = "health"
    INTERNAL_MEMSTATS = "memstats"
    INTERNAL_GATHER = "gather"
    INTERNAL_AGENT = "agent"
    INTERNAL_WRITE = "write"
    ORACLE_MODULES = ['users','tablespaces','sysstat','database','asm','sessions','events','storage','log']

    CORES = 2
    FILE_BUFFER_READ= 1024 * 1024 * 50 #LEEMOS LOS ARCHIVOS EN BLOQUES DE 10MB

    TECHABRV = { "apache": "ap","weblogic": "wl", "tomcat": "to", "jboss": "jb", "mq": "mq", "linux":"lx", "ovo":"ov",
                 "windows": "wi","control":"co", "activemq":"ac","java":"ja","tibco":"ti","unix":"ux","oraclecloud":"oc",
                 "oracle": "or"}

    AGENT=False
    AGENT_PASSWD="97h!$asdfoh230bASDFha-0lpg#od5t(sdi)4#exgijpn6"
    AGENT_BUFFERSIZE=100
    AGENT_CACHE=os.path.join(MONITOR_CACHE,'agent')
    AGENT_CACHEMAXSIZE=1024*1024*20 #20MB: Maximo tamanno de la cache agent
    AGENT_SSL=True

    AGENT_TOKEN_FILE=os.path.join(MONITOR_CACHE,"token.tmp")
    AGENT_CONNECT_TIMEOUT=5
    AGENT_LDB_RANDOM=True
    AGENT_LDB_CROSSCPD=True
    AGENT_LDB_PERSISTENCE=True
    AGENT_LDB_EXPIRE=3600 #Segundos
    LOGSTASH_PASSWD="gr4f4n4"
    #MAXIMO TIEMPO QUE UN PROCESO PUEDE ESTAR EN EJECUCION
    MAX_RUNNING_PROCESS=180
    PTELEGRAF = True

    INTERNAL = {
        "internal_memstats": {
            "alloc_bytes": 0,
            "frees": 0,
            "heap_alloc_bytes": 0,
            "heap_idle_bytes": 0,
            "heap_in_use_bytes": 0,
            "heap_objects_bytes": 0,
            "heap_released_bytes": 0,
            "heap_sys_bytes": 0,
            "mallocs": 0,
            "num_gc": 0,
            "pointer_lookups": 0,
            "sys_bytes": 0,
            "total_alloc_bytes":0
        },
        "internal_agent": {
            "gather_errors": 0,
            "metrics_dropped": 0,
            "metrics_gathered": 0,
            "metrics_written": 0
        },
        "internal_gather":{
            "global":{
                "version": m360.__version__,
                "gather_time_ns": 0,
                "metrics_gathered": 0
            }
        },
        "internal_write":{
            "global":{
                "version": m360.__version__,
                "buffer_limit":0,
                "buffer_size":0,
                "metrics_added":0,
                "metrics_written":0,
                "metrics_dropped":0,
                "metrics_filtered":0,
                "write_time_ns":0
            }
        }
    }
