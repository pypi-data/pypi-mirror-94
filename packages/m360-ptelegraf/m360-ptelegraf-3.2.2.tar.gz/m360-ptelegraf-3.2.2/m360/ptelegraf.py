"""M360 Python agents for Telegraf

Usage:
    ptelegraf --type=[oraclecloud|jboss|weblogic] --config=agent_conf_file --config.d=config_path

"""
import Queue
import datetime
import getpass
import os
import pkgutil
import signal
import socket
import sys
import time
from m360.base.lib.psutilwrapper import stats
import yaml
import pkg_resources
import argparse
import m360
from m360 import agents,outputs,formatter
from m360.base.lib.utils import Utils
from m360.base.settings import Settings
from m360.base.errores import MESSAGES
import logging.handlers
import logging

__defaults = {
    "ptelegraf": {
        "global_tags": {},
        "service": {
            "interval": "60s",
            "debug": False,
            "round_interval": True,
            "metric_batch_size": 1000,
            "metric_buffer_limit": 10000,
            "collection_jitter": "0s",
            "flush_interval": 10,
            "flush_jitter": 0,
            "precision": "ns",
            "hostname": "",
            "quiet": False,
            "logtarget": "file",
            "logfile": "/var/log/telegraf/ptelegraf.log",
            "logfile_rotation_interval": 1,
            "logfile_rotation_max_archives": 5,
            "omit_hostname": False,
            "timeout": "300s"
        }
    }
}

#ALLOWED_MONITORS=[f for f in os.listdir(os.path.join(Settings.MONITOR_PATH,"agents")) if os.path.isdir(os.path.join(Settings.MONITOR_PATH,"agents", f))]
ALLOWED_MONITORS = []
package=agents
for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__, onerror=lambda x: None):
    if ispkg:
        ALLOWED_MONITORS.append(modname)

ALLOWED_OUTPUTS = []
package=outputs
for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__, onerror=lambda x: None):
    if not ispkg:
        ALLOWED_OUTPUTS.append(modname)

ALLOWED_FORMATS = []
package=formatter
for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__, onerror=lambda x: None):
    if not ispkg:
        ALLOWED_FORMATS.append(modname)

#ALLOWED_OUTPUTS=[f.replace(".py","") for f in os.listdir(os.path.join(Settings.MONITOR_PATH,"outputs")) if os.path.isfile(os.path.join(Settings.MONITOR_PATH,"outputs", f)) and f!="__init__.py"]
#ALLOWED_FORMATS=[f.replace(".py","") for f in os.listdir(os.path.join(Settings.MONITOR_PATH,"outputs")) if os.path.isfile(os.path.join(Settings.MONITOR_PATH,"formatter", f)) and f!="__init__.py"]
#ALLOWED_OUTPUTS=['file','graphite','influxdb','stdout']
#ALLOWED_FORMATS=['custom','influx']

l_user = getpass.getuser()

LOG = None

def set_logger(conf=None):
    global LOG
    if LOG is None:
        if conf['logtarget']=="file":
            logfilename = conf['logfile']
            try:
                if not os.path.isdir(os.path.dirname(logfilename)):
                    os.mkdir(os.path.dirname(logfilename),0o755)
                if 'logfile_rotation_interval' in conf:
                    handler = logging.handlers.TimedRotatingFileHandler(logfilename,
                                                                        when='midnight',
                                                                        backupCount=int(conf['logfile_rotation_max_archives']) if 'logfile_rotation_max_archives' in conf else 5)
                elif 'logfile_rotation_max_size' in conf and int(conf['logfile_rotation_max_size']):
                    bytes=int(conf['logfile_rotation_max_size'])*1024*1024*1024
                    handler = logging.handlers.RotatingFileHandler(logfilename,
                                                                   maxBytes=bytes,
                                                                   backupCount=int(conf['logfile_rotation_max_archives']) if 'logfile_rotation_max_archives' in conf else 5)
                else:
                    handler = logging.handlers.WatchedFileHandler(logfilename)
                formatter = logging.Formatter(Settings.LOGFORMAT_DEBUG if conf['debug'] else Settings.LOGFORMAT)
                handler.setFormatter(formatter)
                root = logging.getLogger()
                if conf['debug']:
                    level = logging.DEBUG
                elif conf['quiet']:
                    level = logging.ERROR
                else:
                    level = logging.INFO
                root.setLevel(level)
                root.addHandler(handler)
            except Exception as e:
                pass
        elif conf['logtarget']=="stdout":
            pass

        LOG = logging.getLogger("m360.ptelegraf")
    return LOG

exit = False

def kill_handle(signum, frame):
    global exit
    set_logger().debug("Signal %d received.", signum,extra={'monitor':'ptelegraf','modulo':'main'})
    set_logger().info("Ptelegraf Shutting down...",extra={'monitor':'ptelegraf','modulo':'main'})
    exit = True

def setpid(pidfile):
    if os.path.isfile(pidfile):
        # YA ESTA EJECUTNADOSE UN MONITOR POSIBLEMENTE
        with open(pidfile, 'r') as f:
            oldpid = f.read()
        if oldpid and stats.pid_exists(int(oldpid)):
            set_logger().warning("Ya esta ejecutandose otro agente telegraf (%s)", oldpid,extra={'monitor':'ptelegraf','modulo':'main'})
            return 0
        else:
            set_logger().warning("El agente telegraf (%s) anterior no esta en ejecucion.", oldpid,extra={'monitor':'ptelegraf','modulo':'main'})

    try:
        with open(pidfile, 'w') as f:
            f.write(str(os.getpid()))
    except Exception as e:
        set_logger().error("No se puede escribir el PID (%s). Error (%s).", pidfile,str(e),extra={'monitor':'ptelegraf','modulo':'main'})
        return 0

    return os.getpid()

def get_ptelegraf_service(conf,key):
    if 'ptelegraf' in conf and 'service' in conf['ptelegraf'] and key in conf['ptelegraf']['service']:
        return conf['ptelegraf']['service'][key]
    else:
        return __defaults['ptelegraf']['service'][key]

def get_monitor(monitor):
    for entry_point in pkg_resources.iter_entry_points('ptelegraf.monitors'):
        if entry_point.name == monitor:
            return entry_point.load()
    return None


def get_conf(base,dir=None,types=None,file=None):
    if types is None:
        types = []
    if file:
        try:
            with open(file,'r') as f:
                confObj = yaml.load(f.read(), Loader=yaml.FullLoader)

            ##EL RAIZ debe ser "ptelegraf.<type>"
            for key, val in confObj.items():
                if key == "ptelegraf":
                    base['ptelegraf']=val
                    continue
                _aux,type = key.split(".")
                if _aux not in ["inputs","outputs"]:
                    continue
                if type in types:
                    val['conffile']=file
                    base['inputs'].append({type:val})
                elif type in ALLOWED_OUTPUTS and isinstance(val,dict):
                    base['outputs'].append({type:val})
        except Exception as e:
            print("Failed parse yaml config file '{}'. No monitor loaded. Error:{}".format(file,str(e)))
    elif dir:
        #LISTAMOS TODOS LOS FICHEROS .yaml o yml o subdirectorios
        for f in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, f)):
                base = get_conf(base=base,dir=os.path.join(dir,f),types=types)
            elif os.path.isfile(os.path.join(dir, f)) and (f.endswith(".yaml") or f.endswith(".yml")):
                base = get_conf(base=base,file=os.path.join(dir,f),types=types)
    else:
        print("Failed parse yaml config file. No file or dir conf defined.")

    return base


def main():
    """Main entry point for the script."""
    #CUANTOS COLLECTORES HAY QUE LANZAR
    exit=0
    hostame=socket.gethostname()
    if hasattr(Settings,"HOSTNAME"):
        if Settings.HOSTNAME:
            hostame=Settings.HOSTNAME

    hostname=hostame.split(".")[0]

#    metadata = pkg_resources.get_distribution('m360-ptelegraf')
    parser = argparse.ArgumentParser(description="Monitores python de M360 para Telegraf")
    parser.add_argument('-dir', '--conf-dir', dest='conf_dir',type=str, default=None,
                        help='Config dir for running multiple monitor instances.')
    parser.add_argument('-m','--monitor', type=str, dest='monitor',choices=ALLOWED_MONITORS,
                        help='M360 python monitor technology gather (Jboss,Weblogic,...)')
    parser.add_argument('-c', '--conf', dest='conf_file', type=str, default=None,
                        help='Config file for ptelegraf.')
    parser.add_argument('-d', '--daemon', dest='daemon',action='store_const',const=True,
                        default=False,help='Run as service or daemon.')
    parser.add_argument('-v', '--version', dest='version',action='store_const',const=True,
                        default=False,help='Get M360 Ptelegraf Version.')
    parser.add_argument('-p', '--pid', dest='pidfile',type=str,
                        default=Settings.PIDFILE,help='Ptelegraf pid file.')

    args = parser.parse_args()

    if args.version:
        print(m360.__version__)
        return 0

    if args.conf_file is None and args.conf_dir is None:
        parser.error("at least one of -c or -dir required")
        return (-1)

    _types = ALLOWED_MONITORS
    if args.monitor:
        _types = [args.monitor]
    ptelegraf_conf = {"inputs": [], "outputs": [], "ptelegraf": __defaults['ptelegraf']}
    if args.conf_file:
        conf_file = args.conf_file
        ptelegraf_conf = get_conf(ptelegraf_conf,types=_types, file=conf_file)

    if args.conf_dir:
        ptelegraf_conf = get_conf(ptelegraf_conf,dir=args.conf_dir,types=[] if args.conf_file else _types)

    if not ptelegraf_conf['ptelegraf']:
        print("No ptelegraf conf detected.")
        return(-1)
    set_logger(ptelegraf_conf['ptelegraf']['service'])
    return run(hostname,ptelegraf_conf,args.daemon,args.pidfile)


def run(hostname,ptelegraf_conf,isdaemon,pidfile):
    global exit
    signal.signal(signal.SIGINT, kill_handle)
    signal.signal(signal.SIGTERM, kill_handle)

    if not setpid(pidfile):
        return -1

    ret=0

    if not ptelegraf_conf['inputs']:
        set_logger().warning("No inputs found.",extra={'monitor':'ptelegraf','modulo':'main'})
        return -1

    input_threads_to_start = {}
    loaded_inputs = {}
    queue = None
    for input in ptelegraf_conf['inputs']:
        for monitor,conf in input.items():
            if monitor == "internal":
                queue = Queue.Queue()
        if queue:
            break

    for input in ptelegraf_conf['inputs']:
        for monitor,conf in input.items():
            monitor_class = get_monitor(monitor)
            if monitor_class is None:
                set_logger().error("No '{}' monitor implemented.".format(monitor),
                          extra={'monitor':monitor,'modulo':'main'})
                continue
            try:
                args={"hostname":hostname,"kwargs":{"user":l_user,"settings":conf,"outputs":ptelegraf_conf['outputs'],"service":ptelegraf_conf['ptelegraf']}}
                if queue:
                    args['kwargs']['queue']=queue
                if isdaemon and monitor=="internal":
                    args['kwargs']['loop'] = True
                monitorObj = monitor_class(hostname,**args["kwargs"])
                input_threads_to_start[monitor]=monitorObj
                loaded_inputs[monitor] = { "kwargs": args['kwargs'], "starttime":0 }
            except ImportError as e:
                set_logger().error("Input '%s' defined in '%s' not available. (%s)",monitor,conf['conffile'],str(e),extra={'monitor':'ptelegraf','modulo':'main'})
            except Exception as e:
                set_logger().error("Input '%s' init error. (%s)",monitor,str(e),extra={'monitor':'ptelegraf','modulo':'main'})

    l_threads_not_started = {}
    for name,thread in input_threads_to_start.items():
        try:
            loaded_inputs[name]["starttime"] = time.time()
            thread.start()
            set_logger().debug("Started thread: %s",thread.name,extra={'monitor':'ptelegraf','modulo':'main'})
        except Exception as e:
            l_threads_not_started[name] = thread
            set_logger().error("Thread %s not started. Error %s",name,str(e),extra={'monitor':'ptelegraf','modulo':'main'})

    #VENTANA DE TIEMPO
    interval = Utils.convert_interval(get_ptelegraf_service(ptelegraf_conf,"interval"))
    #TODO: round_interval
    while not exit and isdaemon:
        time.sleep(interval)
        ##TODO: INTERNAL

        #COMPROBAR LOS THREADS TERMINADOS Y VOLVER A ARRANCAR SI HAN PASADO x SEGUNDOS
        for name,t in input_threads_to_start.items():
            if name!="internal" and t.is_alive() and (time.time()-loaded_inputs[name]["starttime"])>Utils.convert_interval(get_ptelegraf_service(ptelegraf_conf,"timeout")):
                ##COMPROBAMOS EL TIEMPO QUE LLEVA LANZADO
                set_logger().error("Thread %s running more than %s. Killing...", name,get_ptelegraf_service(ptelegraf_conf,"timeout"),extra={'monitor': 'ptelegraf', 'modulo': 'main'})
                t.raise_exception()
            if not t.is_alive():
                #LANZAMOS DE NUEVO UN THREAD
                try:
                    monitor_class = get_monitor(name)
                    monitorObj = monitor_class(hostname, **loaded_inputs[name]['kwargs'])
                    input_threads_to_start[name] = monitorObj
                    loaded_inputs[name]["starttime"] = time.time()
                    monitorObj.start()
                    set_logger().debug("Started thread: %s", monitorObj.name,
                                       extra={'monitor': 'ptelegraf', 'modulo': 'main'})
                except Exception as e:
                    set_logger().error("Input '%s' init error. (%s)", name, str(e),
                                       extra={'monitor': 'ptelegraf', 'modulo': 'main'})

    for name,thread in input_threads_to_start.items():
        if isdaemon and name=="internal":
            #force kill
            thread.stop()
        if name not in l_threads_not_started:
            set_logger().debug("Waiting thread '%s' to finish.",thread.name,extra={'monitor':'ptelegraf','modulo':'main'})
            thread.join()

    #REMOVE PID
    try:
        os.remove(pidfile)
    except Exception as e:
        logging.warning("No se pudo eliminar el archivo '%s'.",pidfile,extra={'monitor':'ptelegraf','modulo':'main'})

    set_logger().info("PTelegraf shutdown.",extra={'monitor':'ptelegraf','modulo':'main'})

    return ret

if __name__ == '__main__':
    sys.exit(main())