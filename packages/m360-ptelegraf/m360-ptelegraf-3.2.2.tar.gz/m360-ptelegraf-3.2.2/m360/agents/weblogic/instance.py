# coding=utf-8
from m360.agents.weblogic.settings import Settings
from m360.agents.weblogic.manager import Manager
import m360.base.instance as base
from m360.base.lib.utils import Utils
import time


class Instance (base.Instance):

    ALLOWED_MODULES = [Settings.HTTP,Settings.POOL,Settings.HEAP,Settings.THREADS,Settings.ACCESS,Settings.GC, Settings.JMS,Settings.APP]

    def __init__(self,name,host,conf):
        self._manager = None
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self.data=None
        self._version=None
        self._jvmversion=None
        self._state = None

    #EL HOST DE LA INSTANCIA SE RECUPERA DEL ADMINSERVER Y ES LA MACHINE DONDE ESTA
    @property
    def host(self):
        l_host = self.manager.gethost()
        return self._host if not l_host else l_host

    @property
    def manager(self):
        if not self._manager:
            self._manager=Manager(self)
        return self._manager

    def heap(self):
        data = self.manager.getheapdata()
        return data

    def threads(self):
        return self.manager.getthreadsdata()

    def access(self):
        return Manager.getaccessmetrics(self)

    def pool(self):
        return self.manager.getdatabasepoolsdata()

    def jms(self):
        return self.manager.getjmsdata()

    def http(self):
        return self.manager.getchannelsdata()

    def getjvmversion(self):
        if not self._jvmversion:
            self._jvmversion = self.manager.getjvmversion()
        return self._jvmversion

    def getversion(self):
        if not self._version:
            self._version = self.manager.getWLSversion()
        return self._version

    def gc(self):
        ret = []
        return ret

    def getlogfiles(self):
        if not self._logfiles:
            self._logfiles = []
            logfiles = self.manager.getlogfiles()
            ##Convertimos el formato WL a formato tipo Apache
            for lf in logfiles:
                logformat = lf['format']
                sep=" "
                if logformat:
                    logformat=Utils.parselogformat(Utils.parseWLlogformat(logformat))
                    sep=Utils.logseparator(logformat)
                #TODO: SI ROTA POR NUMMERO DE FICHERO
                lognamepattern = lf['filename'].replace('%yyyy%','%Y')\
                    .replace('%MM%','%m')\
                    .replace('%dd%','%d')\
                    .replace('%hh%','%H')
                #FICHERO ANTERIOR DE LOG ROTADO
                prevlog=Utils.previousRotateFile(lognamepattern,self)
                keypos=Utils.keyposition(logformat,sep)
                if prevlog:
                    #PRIMERO SIEMPRE EL LOG ANTERIOR
                    self._logfiles.append({'host':'localhost',
                                           'lognamepattern':lognamepattern,
                                           'log':prevlog,
                                           'outputmetrics':False, #LAS METRICAS PROCESADAS DE UN LOG ANTERIOR NO SE ENVIAN
                                           'format': logformat,
                                           'keyposition': keypos,
                                           'separator': sep
                                           })

                self._logfiles.append({'host':'localhost',
                                       'lognamepattern':lognamepattern,
                                       'log':time.strftime(lognamepattern,time.localtime()),
                                       'outputmetrics':True, #LAS METRICAS PROCESADAS DE UN LOG ANTERIOR NO SE ENVIAN
                                       'format':logformat,
                                       'separator':sep,
                                       'keyposition':keypos})

        return self._logfiles

    def isrunning(self):
        if Settings.DEBUG:
            return True
        self._state = self.manager.getstate()
        return self._state == "RUNNING"

    def health(self):
        __WL_STATES={"SHUTDOWN":0,"RUNNING":1,"UNKNOWN":0,"STARTING":2,"ADMIN":3,"RESUMING":4,"STANDBY":5,"SUSPENDING":6,"FORCE_SUSPENDING":7,"SHUTTING_DOWN":8}
        ret = self.manager.gethealth()
        ret['status_code'] = __WL_STATES[ret['status']] if ret['status'] in __WL_STATES else -1
        return ret

    def app(self):
        return self.manager.getapps()
