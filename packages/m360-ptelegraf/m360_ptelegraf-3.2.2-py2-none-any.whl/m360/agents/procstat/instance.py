# coding=utf-8
import os
import re
from m360.agents.procstat.settings import Settings
import m360.base.instance as base
from m360.base.lib.psutilwrapper import stats,HPUX,get_processes_by_cmd
import subprocess
from logging import getLogger
from m360.base.lib.utils import Utils

LOG=getLogger('m360.agents.porcstat')


class Instance (base.Instance):

    ALLOWED_MODULES = [Settings.PROCSTAT,Settings.PROCSTAT_LOOKUP]

    def __init__(self,name,host,conf):
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self._version=None

    """
        tags:
            pid (when pid_tag is true)
            cmdline (when 'cmdline_tag' is true)
            process_name
            pidfile (when defined)
            exe (when defined)
            pattern (when defined)
            user (when selected)
            systemd_unit (when defined)
            cgroup (when defined)
            win_service (when defined)
    
        fields:
            child_major_faults (int)
            child_minor_faults (int)
            created_at (int) [epoch in nanoseconds]
            cpu_time (int)
            cpu_time_guest (float)
            cpu_time_guest_nice (float)
            cpu_time_idle (float)
            cpu_time_iowait (float)
            cpu_time_irq (float)
            cpu_time_nice (float)
            cpu_time_soft_irq (float)
            cpu_time_steal (float)
            cpu_time_system (float)
            cpu_time_user (float)
            cpu_usage (float)
            involuntary_context_switches (int)
            major_faults (int)
            memory_data (int)
            memory_locked (int)
            memory_rss (int)
            memory_stack (int)
            memory_swap (int)
            memory_usage (float)
            memory_vms (int)
            minor_faults (int)
            nice_priority (int)
            num_fds (int, telegraf may need to be ran as root)
            num_threads (int)
            pid (int)
            read_bytes (int, telegraf may need to be ran as root)
            read_count (int, telegraf may need to be ran as root)
            realtime_priority (int)
            rlimit_cpu_time_hard (int)
            rlimit_cpu_time_soft (int)
            rlimit_file_locks_hard (int)
            rlimit_file_locks_soft (int)
            rlimit_memory_data_hard (int)
            rlimit_memory_data_soft (int)
            rlimit_memory_locked_hard (int)
            rlimit_memory_locked_soft (int)
            rlimit_memory_rss_hard (int)
            rlimit_memory_rss_soft (int)
            rlimit_memory_stack_hard (int)
            rlimit_memory_stack_soft (int)
            rlimit_memory_vms_hard (int)
            rlimit_memory_vms_soft (int)
            rlimit_nice_priority_hard (int)
            rlimit_nice_priority_soft (int)
            rlimit_num_fds_hard (int)
            rlimit_num_fds_soft (int)
            rlimit_realtime_priority_hard (int)
            rlimit_realtime_priority_soft (int)
            rlimit_signals_pending_hard (int)
            rlimit_signals_pending_soft (int)
            signals_pending (int)
            voluntary_context_switches (int)
            write_bytes (int, telegraf may need to be ran as root)
            write_count (int, telegraf may need to be ran as root)
    """
    def procstat(self):
        data = []
        procs = self.__find_process()
        if procs is None:
            pass
        elif procs:
            pass
        else:
            pass

        return data

    """
    procstat_lookup
        tags:
            exe
            pid_finder
            pid_file
            pattern
            prefix
            user
            systemd_unit
            cgroup
            win_service
            result
        fields:
            min_running: (int, default = 1) 
            pid_count (int)
            running (int)
            result_code (int, success = 0, lookup_error = 1)
    """
    def lookup(self):
        data = Utils.dict_populate(self.conf,
                                   ['exe','pid_finder','pid_file','systemd_unit','cgroup',
                                    'win_service','pattern','prefix','user'])
        data['min_running'] = int(self.conf['min_running']) if 'min_running' in self.conf else 1
        data['pid_count'] = 0
        data['running'] = 0
        data['result_code'] = 0

        procs = self.__find_process()
        if procs is None:
            data['result'] = 'lookup_error'
            data['result_code'] = 1
            return [data]
        elif procs:
            data['result'] = 'success'
            data['pid_count'] = len(procs)
            data['running'] = len(procs)
            pass
        else:
            data['result'] = 'success'
            return [data]
        return data

    def __find_process(self):
        procs = []
        pid = None
        exe = None
        pattern = ''
        user = self.conf['user'] if "user" in self.conf else ''
        if "pid_file" in self.conf:
            try:
                with open(self.conf['pid_file'],'r') as f:
                    pid = int(f.read())
            except Exception as e:
                LOG.warning("Cannot read pidfile. Error: (%s)",str(e),
                            extra={"monitor": "procstat", "modulo": "__find_process"})
                return None
        elif "pattern" in self.conf:
            pattern = self.conf['pattern']
        elif "exe" in self.conf:
            exe = self.conf['exe']
        elif "systemd_unit" in self.conf:
            pass
        elif "win_service" in self.conf:
            pass
        else:
            LOG.warning("No find method defined. (pid_file,pattern,exe,systemd_unit or win_service", extra={"monitor": "procstat", "modulo": "__find_process"})
            return procs

        all_procs = []
        if 'pid_finder' in self.conf and self.conf['pid_finder'] == 'native':
            ##BUSCAMOS CON PSUTIL
            for proc in stats.process_iter():
                try:
                    all_procs.append({"pid":proc.pid,
                                      "user":proc.username(),
                                      "proctitle":" ".join(proc.cmdline()),
                                      "process_name":proc.exe().split(os.path.sep)[-1]})
                except stats.AccessDenied as e:
                    LOG.debug("Access Denied to pid '%d'", proc.pid,
                              extra={"monitor": "procstat", "modulo": "__find_process"})
                except stats.NoSuchProcess as e:
                    LOG.debug("Error getting process. (%s)", str(e), extra={"monitor": "procstat", "modulo": "__find_process"})
                    return None
                except Exception as e:
                    LOG.error("Error getting process. (%s)", str(e),
                              extra={"monitor": "procstat", "modulo": "__find_process"})
                    return None
        else:
            ##BUSCAMOS CON COMANDO
            if 'pid_finder' in self.conf:
                raise NotImplemented("pid_finde conf not implemented yet!")
                #TODO
                #cmd = self.conf['pid_finder'] if isinstance(self.conf['pid_finder'],list) else [self.conf['pid_finder']]
            else:
                cmd = ["ps", '-e', '-o', 'flags,state,user,group,pid,ppid,pgid,nice,ruid,rgid,sz,time,etime,sid,pcpu,args']
            all_procs = get_processes_by_cmd(cmd)

        for p in all_procs:
            try:
                if user=='' or user==p['user']:
                    if pid and pid==p['pid']:
                        procs.append(p)
                    elif exe and exe==p['process_name']:
                        procs.append(p)
                    elif pattern and (p['proctitle'].find(pattern)>=0 or re.search(pattern,p['proctitle'])):
                        procs.append(p)
            except Exception as e:
                LOG.error("Error getting process. (%s)", str(e),
                          extra={"monitor": "procstat", "modulo": "__find_process"})
                return None

        return procs
