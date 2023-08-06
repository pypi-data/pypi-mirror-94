import copy
import datetime
import os
import re
import sys

import m360.base.manager as base
from m360.base.lib.psutilwrapper import stats,HPUX
from m360.base.lib.utils import Utils
import time
from m360.agents.unix.settings import Settings
import subprocess
from logging import getLogger

LOG=getLogger('m360.agents.unix')

_default_conf = {"max": 5}

class Manager (base.Manager):

    @staticmethod
    def getcores():
        if HPUX:
            cpus = stats.cpu_count()
        else:
            try:
                cpus = len(stats.Process().cpu_affinity())
            except Exception as e:
                import multiprocessing
                cpus = multiprocessing.cpu_count()
        return cpus

    @staticmethod
    def getLoad(instance):
        cpus = Manager.getcores()
        if HPUX:
            data = stats.getloadavg()
        else:
            data = os.getloadavg()

        metrics = {'load1': data[0], 'load5': data[1], 'load15': data[2]}
        metrics['n_cpus']=cpus
        metrics['uptime']=int(time.time() - stats.boot_time()) if not HPUX else stats.boot_time()

        try:
            metrics['n_users']=len(stats.users())
        except Exception as e:
            LOG.debug("Cannot read n_users. Error:"+str(e),extra={"monitor": "unix", "modulo": "load"})
        if cpus > 0 :
            metrics['load1percpu'] = float("{0:.2f}".format(data[0]/cpus))
            metrics['load5percpu'] = float("{0:.2f}".format(data[1]/cpus))
            metrics['load15percpu'] = float("{0:.2f}".format(data[2]/cpus))
        return [ metrics ]

    @staticmethod
    def getMemory(instance):
        aux = Utils.toDict(stats.virtual_memory())
        return [aux]

    @staticmethod
    def getSwap(instance):
        aux=  Utils.toDict(stats.swap_memory())
        return [aux]

    @staticmethod
    def getCPU(instance):
        time.sleep(Settings.SLEEP_BEFORE_CPU)
        aux2= stats.cpu_times_percent(interval=Settings.INTERVAL_CPU)
        dataaux=Utils.toDict(aux2)

        #dataaux['percent'] = psutil.cpu_percent(interval=10.0)
        dataaux['usage_active'] = float("{0:.2f}".format(100-dataaux['idle']))
        dataaux['cpu'] = 'cpu-total'
        return [ dataaux ]

    @staticmethod
    def getFilesystems(instance,ignore=None):
        if ignore is None:
            ignore = ["autofs","debugfs","tracefs","configfs","fusectl","hugetlbfs",
                      "pstore","bpf","securityfs","cgroup","cgroup2","tmpfs", "sysfs","mqueue",
                      "devtmpfs", "proc","devpts","devfs", "iso9660", "overlay", "aufs", "squashfs"]
        filesystems = stats.disk_partitions(all=False)
        arradata = []
        for fs in filesystems:
            if fs.fstype in ignore:
                continue
            try:
                data = {}
                if HPUX:
                    data = Utils.toDict(fs)
                else:
                    aux = stats.disk_usage(fs.mountpoint)
                    data['device'] = fs.device
                    data['fstype'] = fs.fstype
                    data['mountpoint'] = fs.mountpoint
                    data['percent'] = aux.percent
                    data['total'] = aux.total
                    data['free'] = aux.free
                    data['used'] = aux.used
                stat = os.statvfs(fs.mountpoint)
                # Python < 3.2
                ST_RDONLY = 1
                readonly = bool(stat.f_flag & ST_RDONLY)
                data['mode'] = "ro" if readonly else "rw"
                arradata.append(data)
            except Exception as e:
                pass
        arradata.extend(Manager.getFiledescriptors(instance))
        return arradata

    @staticmethod
    def getDisk(instance):
        arradata = []
        try:
            disks = stats.disk_io_counters(perdisk=True)
            ignore = ["loop"]
            if 'ignore' in instance.conf:
                ignore = instance.conf['ignore']
            for disk,statstuple in disks.iteritems():
                found = True
                for val in ignore:
                    if disk.lower().find(val) >= 0:
                        found = False
                        break
                if found and 'devices' in instance.conf:
                    found = False
                    for val in instance.conf['devices']:
                        if disk.lower().find(val) >= 0:
                            found = True
                            break
                if not found:
                    continue
                data = Utils.toDict(statstuple)
                data['name'] = disk
                arradata.append(data)
        except Exception as e:
            pass

        return arradata

    @staticmethod
    def getSockets(instance):
        #TODO
        return []

    @staticmethod
    def getFiledescriptors(instance):
        data = []

        if "users" in instance.conf:
            for user in instance.conf["users"]:
                cmd = "lsof -u {}".format(user)
                try:
                    my_env = os.environ.copy()
                    my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
                    LOG.debug("Executed: %s", cmd, extra={"monitor": "linux", "modulo": "fs"})
                    returned_output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT,
                                                              env=my_env,
                                                              universal_newlines=True)
                    file_descriptors=returned_output.split("\n")
                    if len(file_descriptors) > 0:
                        data.append({"user": user,
                                     "fds": len(file_descriptors),
                                     "maxopenfiles": instance.conf['maxopenfiles'] if "maxopenfiles" in instance.conf else 0,
                                     })
                    LOG.debug("Executed: %s", cmd, extra={"monitor": "linux", "modulo": "fs"})
                except subprocess.CalledProcessError as e:
                    LOG.error("Executed: %s ERRCODE: %s ERRMSG: %s", cmd, e.returncode,
                                  Utils.grep(e.output, "exception"),
                                  extra={"monitor": "linux", "modulo": "fs"})
                except Exception as e:
                    LOG.error("Executed: %s ERRMSG: %s", cmd, e.message,
                                  extra={"monitor": "linux", "modulo": "fs"})

        return data

    @staticmethod
    def processes(instance):
        ret = []
        _default = {"blocked": 0, "running": 0, "sleeping": 0, "stopped": 0, "total": 0, "zombies": 0, "dead": 0,
                    "wait": 0, "idle": 0, "paging": 0, "parked": 0, "total_threads": 0 }
        idx=0
        for proc in stats.process_iter():
            try:
                status = proc.status()
                if status == "zombie":
                    status = "zombies"
                if status in _default:
                    _default[status] = _default[status] + 1
                else:
                    LOG.debug("Process status not defined. '%s'",status,extra={"monitor": "unix", "modulo": "processes"})
                _default['total'] = _default['total'] + 1

                ##NO TODOS LOS SO Tienen THREADS ESTO VA AL FINAL
                threads = proc.num_threads()
                _default['total_threads'] = _default['total_threads'] + threads
                idx+=1
            except stats.NoSuchProcess as e:
                LOG.debug("Error getting process. (%s)",str(e),extra={"monitor": "unix", "modulo": "processes"})
            except Exception as e:
                LOG.error("Error getting process status or threads. (%s)",str(e),extra={"monitor": "unix", "modulo": "processes"})

        LOG.debug("End process. Iter %d",idx,extra={"monitor": "unix", "modulo": "processes"})
        ret.append(_default)
        return ret


    @staticmethod
    def getNetwork(instance,ignore=None):
        if ignore is None:
            ignore = ['lo']
        ret = []
        data = stats.net_io_counters(pernic=True)
        for interface,_data in data.items():
            if interface in ignore:
                continue
            data = Utils.toDict(_data)
            data['interface'] = interface
            ret.append(data)

        _data = stats.net_io_counters(pernic=False)
        data = Utils.toDict(_data)
        data['interface'] = "all"
        ret.append(data)
        return ret


    @staticmethod
    def top(instance):
        cpus = Manager.getcores()
        ret = []
        #top
        #[(p.pid, p.info['name'], sum())
        _default = {"blocked": 0, "running": 0, "sleeping": 0, "stopped": 0, "total": 0, "zombies": 0, "dead": 0,
                    "wait": 0, "idle": 0, "paging": 0, "parked": 0, "total_threads": 0 }
        if HPUX:
            i = 1
            procs = []
            for p in stats.get_processes():
                procs.append(copy.deepcopy(p.info))

            processes = sorted(procs,key=lambda p: p['cpu_percent'],reverse=True)
            for p in processes:
                if len(ret) >= _default_conf['max']:
                    break
                ret.append( {"pid":str(p['pid']),
                             "position":i,
                             "name":p['name'],
                             "status":p['status'],
                             "nice": p['nice'],
                             "vms": p['proc_resident'].vms,
                             "rss":p['proc_resident'].rss,
                             "ctime": datetime.timedelta(seconds=sum(p['cpu_times'])).seconds,
                             "username": p['username'],
                             "memory_percent": p['memory_percent'],
                             "cpu_percernt_per_core": p['cpu_percent']/cpus,
                             'cpu_percent':p['cpu_percent']})
                i = i+1
        else:
            for i in [1,2]:
                procs = []
                # Initial call to get base values
                if i == 2:
                    time.sleep(5)
                for p in stats.process_iter():
                    try:
                        p_dict = p.as_dict(['status','cpu_times','username','memory_info', 'nice','memory_percent', 'cpu_percent','name'])
                        p_dict['pid'] = p.pid
                    except stats.NoSuchProcess:
                        pass
                    else:
                        if not p_dict['name'].startswith('ptelegraf'):
                            procs.append(p_dict)

            # return processes sorted by CPU percent usage
            processes = sorted(procs,key=lambda p: p['cpu_percent'],reverse=True)
            i = 1
            for p in processes:
                if len(ret) >= _default_conf['max']:
                    break
                ret.append( {"pid":str(p['pid']),
                             "position":str(i)+'a',
                             "name":p['name'],
                             "status":p['status'],
                             "nice": p['nice'],
                             "vms": p['memory_info'].vms,
                             "rss":p['memory_info'].rss,
                             "ctime": datetime.timedelta(seconds=sum(p['cpu_times'])).seconds,
                             "username": p['username'],
                             "memory_percent": p['memory_percent'],
                             "cpu_percernt_per_core": p['cpu_percent']/cpus,
                             'cpu_percent': p['cpu_percent']})
                i = i+1

        return ret

    @staticmethod
    def netstat(instance):
        ret = []
        data = stats.net_connections(kind='tcp')
        _default_tcp = {"tcp_established": 0, "tcp_syn_sent": 0, "tcp_syn_recv": 0, "tcp_fin_wait1": 0, "tcp_fin_wait2": 0,
                    "tcp_time_wait": 0, "tcp_close": 0, "tcp_close_wait": 0, "tcp_last_ack": 0, "tcp_listen": 0,
                    "tcp_closing": 0, "tcp_none": 0
                    }
        for socket in data:
            status = "tcp_"+socket.status.lower()
            if status in _default_tcp:
                _default_tcp[status] = _default_tcp[status] + 1
            else:
                LOG.warning("TCP status unknown: %s",socket.staus,extra={"monitor": "unix", "modulo": "netstat"})

        data = stats.net_connections(kind='udp')
        if _default_tcp:
            ret.append(_default_tcp)
        if data:
            ret.append({'udp_socket':len(data)})
        return ret

#PROC_NET_NETSTAT
#PROC_NET_SNMP
#PROC_NET_SNMP6
#If these variables are also not set, then it tries to read the proc root from env - PROC_ROOT, and sets /proc as a root path if PROC_ROOT is also empty.

#Then appends default file paths:
#/net/netstat
#/net/snmp
#/net/snmp6

#So if nothing is given, no paths in config and in env vars, the plugin takes the default paths.

#/proc/net/netstat
#/proc/net/snmp
#/proc/net/snmp6
    @staticmethod
    def nstat(instance):
        proc_net_netstat = "/proc/net/netstat"
        proc_net_snmp = "/proc/net/snmp"
        proc_net_snmp6= "/proc/net/snmp6"
        proc_root = ""
        if 'PROC_ROOT' in os.environ:
            proc_root = os.environ['PROC_ROOT']

        if 'proc_net_netstat' in instance.conf:
            proc_net_netstat = instance.conf['proc_net_netstat']
        elif 'PROC_NET_NETSTAT' in os.environ:
            proc_net_netstat = os.environ['PROC_NET_NETSTAT']
        elif proc_root:
            proc_net_netstat = proc_root + "/net/netstat"

        if 'proc_net_snmp' in instance.conf:
            proc_net_snmp = instance.conf['proc_net_snmp']
        elif 'PROC_NET_SNMP' in os.environ:
            proc_net_snmp = os.environ['PROC_NET_SNMP']
        elif proc_root:
            proc_net_snmp = proc_root + "/net/snmp"

        if 'proc_net_snmp6' in instance.conf:
            proc_net_snmp6 = instance.conf['proc_net_snmp6']
        elif 'PROC_NET_SNMP6' in os.environ:
            proc_net_snmp6 = os.environ['PROC_NET_SNMP6']
        elif proc_root:
            proc_net_snmp6 = proc_root + "/net/snmp6"

        l_proc_net_netstat = {}
        if os.path.isfile(proc_net_netstat):
            with open(proc_net_netstat, 'r') as f:
                for line in f:
                    l_array = line.strip().split(" ")
                    if l_array[0] in l_proc_net_netstat:
                        l_proc_net_netstat[l_array[0]] = dict(zip(l_proc_net_netstat[l_array[0]], l_array[1:]))
                    else:
                        l_proc_net_netstat[l_array[0]] = [l_array[0].replace(":","")+val for val in l_array[1:]]
        else:
            LOG.warning("No snmp file '%s'. Disable plugin!",proc_net_snmp,extra={"monitor": "unix", "modulo": "nstat"})

        l_proc_net_snmp = {}
        if os.path.isfile(proc_net_snmp):
            with open(proc_net_snmp, 'r') as f:
                for line in f:
                    l_array = line.strip().split(" ")
                    if l_array[0] in l_proc_net_snmp:
                        l_proc_net_snmp[l_array[0]] = dict(zip(l_proc_net_snmp[l_array[0]], l_array[1:]))
                    else:
                        l_proc_net_snmp[l_array[0]] = [l_array[0].replace(":","")+val for val in l_array[1:]]
        else:
            LOG.warning("No snmp file '%s'. Disable plugin!",proc_net_snmp,extra={"monitor": "unix", "modulo": "nstat"})

        l_proc_net_snmp6 = {}
        if os.path.isfile(proc_net_snmp6):
            with open(proc_net_snmp6, 'r') as f:
                for line in f:
                    line2 = re.sub('\s+', ' ', line).strip()
                    l_array = line2.split(" ")
                    l_proc_net_snmp6[l_array[0]]=l_array[1]
        else:
            LOG.warning("No snmp6 file '%s'. Disable plugin!",proc_net_snmp6,extra={"monitor": "unix", "modulo": "nstat"})

        ret = []
        if l_proc_net_snmp6:
            nval=copy.deepcopy(l_proc_net_snmp6)
            nval['name']="snmp6"
            ret.append(nval)
        for key, l_values in l_proc_net_snmp.iteritems():
            nval=copy.deepcopy(l_values)
            nval['name']="snmp"
            ret.append(nval)
        for key, l_values in l_proc_net_netstat.iteritems():
            nval=copy.deepcopy(l_values)
            nval['name']="netstat"
            ret.append(nval)

        return ret

def popen_tty(cmd,passwd):
    import subprocess
    """Open a process with stdin connected to a pseudo-tty.  Returns a

    :param cmd: command to run
    :type cmd: str
    :returns: (Popen, master) tuple, where master is the master side
       of the of the tty-pair.  It is the responsibility of the caller
       to close the master fd, and to perform any cleanup (including
       waiting for completion) of the Popen object.
    :rtype: (Popen, int)

    """

    import pty
    master, slave = pty.openpty()
    cmd1 = subprocess.Popen(['echo', passwd],stdout=subprocess.PIPE)
    proc = subprocess.Popen(cmd,
                            stdin=cmd1.stdout,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            preexec_fn=os.setsid,
                            close_fds=True,
                            shell=True)
    os.close(slave)

    return (proc, master)

