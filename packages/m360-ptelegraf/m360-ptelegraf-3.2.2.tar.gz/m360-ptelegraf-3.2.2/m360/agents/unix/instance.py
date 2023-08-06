# coding=utf-8
import m360.base.instance as base
from m360.agents.unix.settings import  Settings
from m360.agents.unix.manager import Manager
import platform

class Instance (base.Instance):

    ALLOWED_MODULES = [ Settings.NSTAT, Settings.NETSTAT,Settings.PROCESSES, Settings.CPU, Settings.TOP,Settings.MEMORY, Settings.SWAP, Settings.DISK, Settings.SYSTEM, Settings.NETWORK, Settings.DISKIO ]

    def __init__(self,name,host,conf):
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self._version = platform.platform()
        self.global_tags.pop('instance',None)

    def getindexpath(self):
        return self._indexpath

    def cpu(self):
        data = Manager.getCPU(self)
        return data

    def net(self):
        data = Manager.getNetwork(self)
        return data

    def diskio(self):
        data = Manager.getDisk(self)
        return data

    def disk(self):
        data = Manager.getFilesystems(self)
        return data

    def mem(self):
        data = Manager.getMemory(self)
        return data

    def swap(self):
        data = Manager.getSwap(self)
        return data

    def system(self):
        data = Manager.getLoad(self)
        return data

    def processes(self):
        data= Manager.processes(self)
        return data

    def top(self):
        data= Manager.top(self)
        return data

    def nstat(self):
        data= Manager.nstat(self)
        return data

    def netstat(self):
        data= Manager.netstat(self)
        return data