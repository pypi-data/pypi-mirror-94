import copy
import os
import re
import sys
import time
from collections import namedtuple
from m360.base.settings import Settings
from logging import getLogger
import platform
import subprocess

LOG=getLogger('m360.base.lib.psutilwrapper')

HPUX = Settings.DEBUG_HPUX or ( True if sys.platform.startswith("hp-ux11") else False )
HPUX_PA_RISC = False
if Settings.DEBUG_HPUX or platform.machine().startswith("9000"):
    HPUX_PA_RISC = True

def parse_unix_ps_time_to_epoch(strdatetime):
    strdias = 0
    strhora = 0
    strmin = 0
    strsegs = 0
    if strdatetime.find("-") >= 0:
        strdias, strtime = strdatetime.split("-")
        strhora, strmin, strsegs = strtime.split(":")
    else:
        strtime = strdatetime.split(":")
        if len(strtime) == 1:
            strsegs = strtime[0]
        elif len(strtime) == 2:
            strmin = strtime[0]
            strsegs = strtime[1]
        elif len(strtime) == 3:
            strhora = strtime[0]
            strmin = strtime[1]
            strsegs = strtime[2]
    return int(strdias) * 60 * 60 * 24 + int(strhora) * 60 * 60 + int(strmin) * 60 + int(strsegs)

#HP-UX
_PS_STATES_HP_UX = {
    "0": 4,
    "S": 1,
    "W": 5,
    "R": 0,
    "I": 4,
    "Z": 3,
    "T": 2,
    "X": 4
}
def _PS_STATES_HP_UX_GET(psutil_key):
    return _PS_STATES_HP_UX[psutil_key] if psutil_key in _PS_STATES_HP_UX else 4

def get_processes_by_cmd(cmd,cols=None):
    ret = []
    my_env = os.environ.copy()
    my_env["UNIX95"] = ""
    ps = subprocess.Popen(cmd,
                          env=my_env,
                          stdout=subprocess.PIPE)
    stdout, stderr = ps.communicate()
    if stderr is None:
        processes = stdout.split("\n")
        cols = [n for n in processes[0].split()]
        for process in processes[1:]:
            paux = process.split()
            if not paux:
                continue
            _start_time = parse_unix_ps_time_to_epoch(paux[12])
            _time_spent = parse_unix_ps_time_to_epoch(paux[11])
            _proc_title = " ".join(paux[15:])
            _process_name = paux[15]
            _attrs = {
                'pid': int(paux[4]),
                'euid': int(paux[8]),
                'egid': int(paux[9]),
                'parent': int(paux[5]),
                'pgid': int(paux[6]),
                'start_time': _start_time,
                'time_spent': _time_spent,
                'proctitle': _proc_title,
                'proc_size': long(paux[10]),
                'nice': int(paux[7]) if paux[7] != "-" else 0,
                'process_name': _process_name,
                'user': paux[2] if 'USER' in cols else int(paux[2]),
                'group': paux[3] if 'GROUP' in cols else int(paux[3]),
                'uid': int(paux[2]) if 'UID' in cols else paux[2],
                'gid': int(paux[3]) if 'GID' in cols else paux[3],
                'sessid': int(paux[13]),
                'involuntary_context_switches': 0L,
                'context_switches': 0L,
                'voluntary_context_switches': 0L,
                'cpu_percent': float(paux[14]),
                'proc_resident': 0L,
                'state': _PS_STATES_HP_UX_GET(paux[1])
            }
            ret.append(_attrs)
    else:
        LOG.error("Error executing '%s'. (%s)", " ".join(cmd), stderr,
                  extra={"monitor": "statgrab", "modulo": "Process"})
    return ret


if HPUX:
    import statgrab
    from m360.base.lib.netstat import Netstat

    if not HPUX_PA_RISC:
        statgrab.init()

    _PS_FLAGS_HP_UX = {
        "0":"Swapped",
        "1":"In core",
        "2":"System",
        "4":"Locked in core",
        "10":"Being traced",
        "20":"Tracing"
    }

    _STATGRAB_PSUTIL_PROCESS_STATUS = ["running", "sleeping", "stopped", "zombie", "unknown","wait"]

    _STATGRAB_PSUTIL_PROCESS={
        "start_time":"create_time",
        "proctitle":"cmdline",
        "process_name":"name",
        "state":"status",
        "time_spent": "cpu_times"
    }

    _STATGRAB_PS_STATGRAB={
        "start_time":"create_time",
        "proctitle":"cmdline",
        "process_name":"name",
        "state":"status",
        "time_spent": "cpu_times"
    }

    _PSUTIL_STATGRAB_PROCESS={
        "create_time":"start_time",
        "cmdline":"proctitle",
        "name":"process_name",
        "status":"state",
        "cpu_times": "time_spent"
    }

    _STATGRAB_PSUTIL_PARTITION={
        "device_name":"name",
        "fs_type":"fstype",
        "mnt_point":"mountpoint",
        "device_canonical":"device",
        "size":"total"
    }

    _STATGRAB_PSUTIL_NET={
        "ierrors":"errin",
        "oerrors":"errout",
        "rx":"bytes_recv",
        "tx":"bytes_sent",
        "opackets":"packtes_sent",
        "ipackets":"packets_recv"
    }

    _STATGRAB_PSUTIL_DISK={
    }

    def _STATGRAB_PSUTIL_DISK_GET(psutil_key):
        return _STATGRAB_PSUTIL_DISK[psutil_key] if psutil_key in _STATGRAB_PSUTIL_DISK else psutil_key

    def _PSUTIL_STATGRAB_PROCESS_GET(psutil_key):
        return _PSUTIL_STATGRAB_PROCESS[psutil_key] if psutil_key in _PSUTIL_STATGRAB_PROCESS else psutil_key

    def _STATGRAB_PSUTIL_PARTITION_GET(psutil_key):
        return _STATGRAB_PSUTIL_PARTITION[psutil_key] if psutil_key in _STATGRAB_PSUTIL_PARTITION else psutil_key

    def _STATGRAB_PSUTIL_NET_GET(psutil_key):
        return _STATGRAB_PSUTIL_NET[psutil_key] if psutil_key in _STATGRAB_PSUTIL_NET else psutil_key

    class StatgrabPsutil():
        class Error(Exception):
            """Base exception class. All other psutil exceptions inherit
            from this one.
            """
            __module__ = 'psutilwrapper'

            def __init__(self, msg=""):
                Exception.__init__(self, msg)
                self.msg = msg

            def __repr__(self):
                ret = "psutilwrapper.%s %s" % (self.__class__.__name__, self.msg)
                return ret.strip()

            __str__ = __repr__

        class NoSuchProcess(Error):
            """Exception raised when a process with a certain PID doesn't
            or no longer exists.
            """
            __module__ = 'psutilwrapper'

            def __init__(self, pid, name=None, msg=None):
                StatgrabPsutil.Error.__init__(self, msg)
                self.pid = pid
                self.name = name
                self.msg = msg
                if msg is None:
                    if name:
                        details = "(pid=%s, name=%s)" % (self.pid, repr(self.name))
                    else:
                        details = "(pid=%s)" % self.pid
                    self.msg = "process no longer exists " + details

        class AccessDenied(Error):
            """Exception raised when a process with a certain PID doesn't
            or no longer exists.
            """
            __module__ = 'psutilwrapper'

            def __init__(self, pid, name=None, msg=None):
                StatgrabPsutil.Error.__init__(self, msg)
                self.pid = pid
                self.name = name
                self.msg = msg
                if msg is None:
                    if name:
                        details = "(pid=%s, name=%s)" % (self.pid, repr(self.name))
                    else:
                        details = "(pid=%s)" % self.pid
                    self.msg = "access denied to process " + details

        @staticmethod
        def available_cpu_count():
            """ Number of available virtual or physical CPUs on this system, i.e.
            user/real as output by time(1) when called with an optimally scaling
            userspace-only program"""

            # cpuset
            # cpuset may restrict the number of *available* processors
            try:
                m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                              open('/proc/self/status').read())
                if m:
                    res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
                    if res > 0:
                        return res
            except IOError:
                pass

            # POSIX
            try:
                res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

                if res > 0:
                    return res
            except (AttributeError, ValueError):
                pass

            # Windows
            try:
                res = int(os.environ['NUMBER_OF_PROCESSORS'])

                if res > 0:
                    return res
            except (KeyError, ValueError):
                pass

            # jython
            try:
                from java.lang import Runtime
                runtime = Runtime.getRuntime()
                res = runtime.availableProcessors()
                if res > 0:
                    return res
            except ImportError:
                pass

            # BSD
            try:
                sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                          stdout=subprocess.PIPE)
                scStdout = sysctl.communicate()[0]
                res = int(scStdout)

                if res > 0:
                    return res
            except (OSError, ValueError):
                pass

            # Linux
            try:
                res = open('/proc/cpuinfo').read().count('processor\t:')

                if res > 0:
                    return res
            except IOError:
                pass

            # Solaris
            try:
                pseudoDevices = os.listdir('/devices/pseudo/')
                res = 0
                for pd in pseudoDevices:
                    if re.match(r'^cpuid@[0-9]+$', pd):
                        res += 1

                if res > 0:
                    return res
            except OSError:
                pass

            # Other UNIXes (heuristic)
            try:
                try:
                    dmesg = open('/var/run/dmesg.boot').read()
                except IOError:
                    dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
                    dmesg = dmesgProcess.communicate()[0]

                res = 0
                while '\ncpu' + str(res) + ':' in dmesg:
                    res += 1

                if res > 0:
                    return res
            except OSError:
                pass

            # HP-UX
            try:
                sysctl = subprocess.Popen(['/usr/sbin/ioscan', '-kf'], stdout=subprocess.PIPE)
                grep = subprocess.Popen(['grep', 'processor'], stdin=sysctl.stdout, stdout=subprocess.PIPE)
                count = subprocess.Popen(['wc', '-l'], stdin=grep.stdout, stdout=subprocess.PIPE)
                end_of_pipe = count.stdout
                for line in end_of_pipe:
                    return int(line.strip())

            except Exception as e:
                pass

            raise Exception('Can not determine number of CPUs on this system')

        @staticmethod
        def cpu_count():
            info = statgrab.get_host_info() if not HPUX_PA_RISC else statgrab.sg_get_host_info()
            try:
                return info.ncpus
            except Exception as e:
                return StatgrabPsutil.available_cpu_count()

        @staticmethod
        def getloadavg():
            data = statgrab.get_load_stats() if not HPUX_PA_RISC else statgrab.sg_get_load_stats()
            return [data['min1'],data['min5'],data['min15']]

        @staticmethod
        def process_iter(attrs=None):
            results = StatgrabPsutil.get_processes(attrs)
            for r in results:
                yield r

        @staticmethod
        def get_processes(attrs=None):
            ret = []
            #TODO
            if not HPUX_PA_RISC and False:
                results = statgrab.get_process_stats()
                for r in results:
                    if attrs:
                        only_attr = {}
                        for a in attrs:
                            aux=_PSUTIL_STATGRAB_PROCESS_GET(a)
                            only_attr[aux] = r.attrs[aux]
                    else:
                        only_attr = r.attrs

                    p = StatgrabPsutil.Process(**only_attr)
                    ret.append(p)
            else:
                cmd = ["ps",'-e','-o','flags,state,uid,gid,pid,ppid,pgid,nice,ruid,rgid,sz,time,etime,sid,pcpu,args']
                ps = get_processes_by_cmd(cmd)
                for p in ps:
                    ret.append(StatgrabPsutil.Process(**p))
            return ret

        @staticmethod
        def pid_exists(pid):
            results = StatgrabPsutil.get_processes()
            for p in results:
                if p.pid==pid:
                    return p
            return False

        @staticmethod
        def users():
            result = subprocess.check_output(['who']).decode('utf-8')

            users = []
            for line in result.splitlines():
                name = line.split()[0]
                if name not in users:
                    users.append(name)

            return users

        @staticmethod
        def virtual_memory():
            result = statgrab.get_mem_stats() if not HPUX_PA_RISC else statgrab.sg_get_mem_stats()
            ret = result.attrs
            ret['percent'] = 100.0-100.0*(float(result.free)/float(result.total))
            ret.pop('systime',None)
            return ret

        @staticmethod
        def swap_memory():
            result = statgrab.get_swap_stats() if not HPUX_PA_RISC else statgrab.sg_get_swap_stats()
            ret = result.attrs
            ret['percent'] = 100.0*(float(result.used)/float(result.total))
            ret.pop('systime',None)
            result = statgrab.get_page_stats() if not HPUX_PA_RISC else statgrab.sg_get_page_stats()
            ret['sin'] = result.pages_pagein
            ret['sout'] = result.pages_pageout
            return ret

        @staticmethod
        def cpu_times_percent(interval=0):
            result = statgrab.get_cpu_percents() if not HPUX_PA_RISC else statgrab.sg_get_cpu_percents()
            if interval:
                time.sleep(interval)
                result = statgrab.get_cpu_percents() if not HPUX_PA_RISC else statgrab.sg_get_cpu_percents()
            ret=result.attrs
            ret['system']=ret['kernel']
            ret.pop('kernel')
            ret.pop('time_taken',None)
            ret.pop('swap',None)
            return ret

        @staticmethod
        def disk_usage(path):
            raise NotImplemented

        @staticmethod
        def disk_io_counters(perdisk=False):
            ret={}
            total={}
            results = statgrab.get_disk_io_stats()  if not HPUX_PA_RISC else statgrab.sg_get_disk_io_stats()
            time.sleep(5)
            results = statgrab.get_disk_io_stats_diff()  if not HPUX_PA_RISC else statgrab.sg_get_disk_io_stats_diff()
            for r in results:
                ret[r.disk_name] = {}
                for k,v in r.attrs.items():
                    if k not in ["disk_name","systime"]:
                        ret[r.disk_name][_STATGRAB_PSUTIL_DISK_GET(k)]=v
                        if _STATGRAB_PSUTIL_DISK_GET(k) not in total:
                            total[_STATGRAB_PSUTIL_DISK_GET(k)]=0
                        total[_STATGRAB_PSUTIL_DISK_GET(k)]=total[_STATGRAB_PSUTIL_DISK_GET(k)]+v
            return ret if perdisk else total

        @staticmethod
        def disk_partitions(all=True):
            ret=[]
            results = statgrab.get_fs_stats()  if not HPUX_PA_RISC else statgrab.sg_get_fs_stats()
            if results:
                fields = ['percent']
                for k, v in results[0].attrs.items():
                    fields.append(_STATGRAB_PSUTIL_PARTITION_GET(k))
                if "systime" in fields: fields.remove("systime")
                p=namedtuple('Partition',fields)
                for part in results:
                    part.attrs.pop('systime',None)
                    attrs = {}
                    for k, v in part.attrs.items():
                        attrs[_STATGRAB_PSUTIL_PARTITION_GET(k)] = v
                    attrs['percent']=100*(float(part.used)/float(part.size)) if part.size else 0.0
                    ret.append(p(**attrs))
            return ret

        @staticmethod
        def net_io_counters(pernic=True):
            ret={}
            total={}
            results = statgrab.get_network_io_stats()  if not HPUX_PA_RISC else statgrab.sg_get_network_io_stats()
            for r in results:
                ret[r.interface_name] = {}
                for k,v in r.attrs.items():
                    if k not in ["interface_name","systime"]:
                        ret[r.interface_name][_STATGRAB_PSUTIL_NET_GET(k)]=v
                        if _STATGRAB_PSUTIL_NET_GET(k) not in total:
                            total[_STATGRAB_PSUTIL_NET_GET(k)]=0
                        total[_STATGRAB_PSUTIL_NET_GET(k)]=total[_STATGRAB_PSUTIL_NET_GET(k)]+v
            return ret if pernic else total

        @staticmethod
        def net_connections(kind='tcp'):
#            results = Netstat.netstat(kind) <<<<<<< NOT WORKING UNIX
            results = []
            return results

        @staticmethod
        def boot_time():
            info = statgrab.get_host_info()  if not HPUX_PA_RISC else statgrab.sg_get_host_info()
            return info.uptime

        class Process():
            # 'proctitle' = {str}
            # 'pgid' = {int}
            # 'uid' = {int}
            # 'parent' = {int}
            # 'pid' = {int}
            # 'start_time' = {int}
            # 'process_name' = {str}
            # 'context_switches' = {long}
            # 'time_spent' = {int}
            # 'euid' = {int}
            # 'proc_resident' = {long}
            # 'proc_size' = {long}
            # 'egid' = {int}
            # 'voluntary_context_switches' = {long}
            # 'cpu_percent' = {float}
            # 'involuntary_context_switches' = {long}
            # 'state' = {int}
            # 'sessid' = {int}
            # 'systime' = {int}
            # 'gid' = {int}
            # 'nice' = {int}

            def __init__(self,**kwargs):
                if 'pid' in kwargs:
                    self._pid = int(kwargs['pid'])
                _attr = None
                if 'pid' not in kwargs or len(kwargs)>1:
                    _attr = copy.deepcopy(kwargs)
                elif 'pid' in kwargs:
                    ##SOLO TENEMOS EL PID BUSCAMOS EL PROCESO
                    _attr = StatgrabPsutil.pid_exists(self._pid)
                if not _attr:
                    raise StatgrabPsutil.NoSuchProcess(self._pid)
                else:
                    # PSUTIL COMPAT
                    self._attr=self.PSUTIL_PROCESS_MAP_COMPAT(_attr)

            @staticmethod
            def PSUTIL_PROCESS_MAP_COMPAT(attr):
                newattr={}
                for key,val in attr.items():
                    if key in _STATGRAB_PSUTIL_PROCESS:
                        nkey = _STATGRAB_PSUTIL_PROCESS[key]
                        if nkey == "cmdline":
                            val = val.split()
                        elif nkey=="status":
                            val = _STATGRAB_PSUTIL_PROCESS_STATUS[min(int(val),len(_STATGRAB_PSUTIL_PROCESS_STATUS)-1)]
                        newattr[nkey]=val
                    else:
                        newattr[key] = val

                return newattr

            def __getattr__(self, name):
                def method(*args):
                    if args:
                        raise StatgrabPsutil.Error(name + " had arguments: " + str(args))
                    if name in self._attr:
                        return self._attr[name]
                    else:
                        LOG.debug("Process func not defined. '%s'", name,
                                  extra={"monitor": "statgrab", "modulo": "Process"})
                        return 0
                if name=="info":
                    return self._attr
                return method

    stats=StatgrabPsutil
else:
    import psutil
    stats=psutil

