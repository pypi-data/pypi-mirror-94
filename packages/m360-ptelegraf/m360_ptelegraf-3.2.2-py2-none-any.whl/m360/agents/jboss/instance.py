# coding=utf-8
import m360.base.instance as base
from m360.agents.jboss.settings import  Settings
from m360.agents.jboss.manager import Manager
import os
from logging import getLogger
import time
from m360.base.lib.utils import Utils

LOG=getLogger('m360.agents.jboss')

class Instance (base.Instance):

    ALLOWED_MODULES = [Settings.HTTP,Settings.POOL,Settings.HEAP,Settings.THREADS,Settings.ACCESS,Settings.GC]

    def __init__(self,name,host,conf):
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self.data=None
        self._version=None
        self._jvmversion=None
        self._version=conf['version'] if 'version' in conf else ""
        self._jvmversion = conf['jvmversion'] if 'jvmversion' in conf else ""

    def getdata(self):
        if self.data == None:
            if self.version.startswith("6"):
                self.data = Manager.server_jmx(self.conf['endpoint'],
                                               self.conf['user'],
                                               self.conf['passwd'],
                                               majorversion="jre7" if self.jvmversion.find("1.7") >= 0 or self.jvmversion.find("1.8") >= 0 else "jre6")
            elif self.version.startswith("7"):
                self.data = Manager.server_jmx7EAP(self.conf['endpoint'],
                                               self.conf['user'],
                                               self.conf['passwd'])
            else:
                self.data = Manager.server_status(self.conf['endpoint'],self.conf['user'],self.conf['passwd'])
        return self.data

    @property
    def jvmversion(self):
        return self._jvmversion

    def getjvmversion(self):
        return self.jvmversion

    def heap(self):
        arrmetrics=[]
        try:
            data = self.getdata()
            if 'jvm' in data['status']:
                arrmetrics.append(data['status']['jvm']['memory'])
        except Exception as e:
            LOG.error("Error %s", e.message,extra={"monitor":self.tech,"modulo":"heap"})

        return arrmetrics

    def threads(self):
        arrmetrics=[]
        try:
            data = self.getdata()
            if 'connector' in data['status']:
                if isinstance(data['status']['connector'],dict):
                    metrics = data['status']['connector']['threadInfo']
                    metrics['name'] = data['status']['connector']['name']
                    arrmetrics.append(metrics)
                elif isinstance(data['status']['connector'],list):
                    for c in data['status']['connector']:
                        metrics = c['threadInfo']
                        metrics['name'] = c['name']
                        arrmetrics.append(metrics)
        except Exception as e:
            LOG.error("Error %s", e.message,extra={"monitor":self.tech,"modulo":"threads"})
        return arrmetrics

    def pool(self):
        data = []
        datasourcesBean = {}
        #name=DefaultDS,service=ManagedConnectionPool
        if self.version.startswith("6"):
            datasourcesBean = Manager.server_jmx(self.conf['endpoint'],
                                          self.conf['user'],
                                          self.conf['passwd'],
                                          majorversion="jre7" if self.jvmversion.find("1.7")>=0 or self.jvmversion.find("1.8") >= 0 else "jre6",
                                          beanname="/subsystem=datasources",recursive="true")

        elif self.version.startswith("5") or self.version.startswith("4"):
            datasourcesBean = Manager.server_jmx(self.conf['endpoint'],
                                                self.conf['user'],
                                                self.conf['passwd'],
                                                ip=self.conf['ip'],
                                                jmxport=self.conf['jmxport'],
                                                pool=True,
                                                majorversion=self.version[0],
                                                java=self.conf["javaruntime"])
        elif self.version.startswith("7"):
            dataaux = self.getdata()
            datasourcesBean=dataaux['status']

        if datasourcesBean and "data-source" in datasourcesBean and datasourcesBean['data-source']:
            for dsname, dsstats in datasourcesBean['data-source'].iteritems():
                arrmetrics = dsstats['statistics']['pool']
                arrmetrics['PoolName'] = dsname
                data.append(arrmetrics)

        return data

    def access(self):
        data=Manager.getaccessmetrics(self)
        return data

    def http(self):
        arrmetrics=[]
        try:
            data = self.getdata()
            if 'connector' in data['status']:
                if isinstance(data['status']['connector'],dict):
                    metrics = data['status']['connector']['requestInfo']
                    metrics['name'] = data['status']['connector']['name']
                    arrmetrics.append(metrics)
                elif isinstance(data['status']['connector'],list):
                    for c in data['status']['connector']:
                        metrics = c['requestInfo']
                        metrics['name'] = c['name']
                        arrmetrics.append(metrics)
        except Exception as e:
            LOG.error("Error %s", e.message,extra={"monitor":self.tech,"modulo":"http"})
        return arrmetrics

    def getlogfiles(self):
        ##BUSCAMOS LA CARPETA DE LOGS
        logtuplatmp = {}
        lognamepattern = None
        if not self._logfiles:
            if self.version.startswith("6"):
                # JBOSS6
                acesslogBean = Manager.server_jmx(self.conf['endpoint'],
                                                  self.conf['user'],
                                                  self.conf['passwd'],
                                                  beanname="/subsystem=web/virtual-server=default-host/access-log=configuration")
                if acesslogBean:
                    enviroment = Manager.server_jmx(self.conf['endpoint'],
                                                      self.conf['user'],
                                                      self.conf['passwd'],
                                                      beanname="/core-service=server-environment")
                    suffix=time.strftime("%Y-%m-%d",time.localtime())
                    suffix2="%Y-%m-%d"
                    if 'rotate' in acesslogBean and not acesslogBean['rotate']:
                        suffix=""
                        suffix2=""
                    lognamepattern=os.path.join(enviroment['log-dir'],acesslogBean['prefix']+suffix2)
                    logtuplatmp = {'host': 'localhost',
                                        'log':os.path.join(enviroment['log-dir'],
                                                           acesslogBean['prefix']+suffix), #JBOSS6 SUFFIX)
                                        'format':acesslogBean['pattern'] if 'pattern' in acesslogBean else ""}
            elif self.version.startswith("7"):
                data=self.getdata()
                suffix=time.strftime("%Y-%m-%d",time.localtime())
                suffix2="%Y-%m-%d"
                if 'rotate' in data['status']['logbean'] and not data['status']['logbean']['rotate']:
                    suffix=""
                    suffix2=""
                if 'log-dir' in data['status']['logbean']:
                    lognamepattern=os.path.join(data['status']['logbean']['log-dir'],data['status']['logbean']['prefix']+suffix2)
                    logtuplatmp = {'host': 'localhost',
                                        'log':os.path.join(data['status']['logbean']['log-dir'],
                                                           data['status']['logbean']['prefix']+suffix), #JBOSS6 SUFFIX)
                                        'format':data['status']['logbean']['pattern'] if 'pattern' in data['status']['logbean'] else ""}
            else:
                # >= JBOSS4.2
                valvebeanname = "jboss.web:host=localhost,name=AccessLogValve,type=Valve"
                acesslogBean = Manager.server_jmx(self.conf['endpoint'],
                                                  self.conf['user'],
                                                  self.conf['passwd'],
                                                  access=True,
                                                  majorversion=self.version[0],
                                                  ip=self.conf['ip'],
                                                  jmxport=self.conf['jmxport'],
                                                  java=self.conf['javaruntime'],
                                                  beanname=valvebeanname)
                if not acesslogBean or valvebeanname not in acesslogBean:
                    valvebeanname = "jboss.web:host=localhost,name=FastCommonAccessLogValve,type=Valve"
                    acesslogBean = Manager.server_jmx(self.conf['endpoint'],
                                                      self.conf['user'],
                                                      self.conf['passwd'],
                                                      access=True,
                                                      majorversion=self.version[0],
                                                      ip=self.conf['ip'],
                                                      jmxport=self.conf['jmxport'],
                                                      java=self.conf['javaruntime'],
                                                      beanname=valvebeanname)

                if acesslogBean and valvebeanname in acesslogBean:
                    lognamepattern=os.path.join(acesslogBean[valvebeanname]['directory'],
                                                           acesslogBean[valvebeanname]['prefix'] +
                                                           "%Y-%m-%d"+
                                                           acesslogBean[valvebeanname]['suffix'])
                    logtuplatmp = {'host': 'localhost',
                                       'log': os.path.join(acesslogBean[valvebeanname]['directory'],
                                                           acesslogBean[valvebeanname]['prefix'] +
                                                           time.strftime("%Y-%m-%d",time.localtime())+
                                                           acesslogBean[valvebeanname]['suffix']),
                                       # JBOSS6 SUFFIX)
                                       'format': acesslogBean[valvebeanname]['pattern'] if 'pattern' in acesslogBean[valvebeanname] else ""}
            if logtuplatmp:
                logtuplatmp['outputmetrics']=True
                logtuplatmp['lognamepattern']=lognamepattern
                logtuplatmp['format']=Utils.parselogformat(logtuplatmp['format'])
                logtuplatmp['separator'] = Utils.logseparator(logtuplatmp['format'])
                logtuplatmp['keyposition']=Utils.keyposition(logtuplatmp['format'],logtuplatmp['separator'])
                #FICHERO ANTERIOR DE LOG ROTADO
                #incluimos el log anterior en hora o dia si no se ha terminado de procesar
                prevlog=Utils.previousRotateFile(lognamepattern,self)
                self._logfiles = []
                if prevlog:
                    #PRIMERO SIEMPRE EL LOG ANTERIOR
                    self._logfiles.append({'host':logtuplatmp['host'],
                                           'lognamepattern':lognamepattern,
                                           'log':prevlog,
                                           'outputmetrics':False, #LAS METRICAS PROCESADAS DE UN LOG ANTERIOR NO SE ENVIAN
                                           'format': logtuplatmp['format'],
                                           'keyposition': logtuplatmp['keyposition'],
                                           'separator': logtuplatmp['separator']
                                           })

                self._logfiles.append(logtuplatmp)

        return self._logfiles

    def isrunning(self):
        ret=False
        try:
            ret = not self.getdata() is None
        except Exception as e:
            LOG.error("Error %s", str(e),extra={"monitor":self.tech,"modulo":"isrunning"})
            ret = False
        return ret
