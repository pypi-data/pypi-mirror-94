# coding=utf-8
import m360.base.instance as base
from m360.agents.tomcat.settings import Settings
from m360.agents.tomcat.manager import Manager
import os
from logging import getLogger
import time
from m360.base.lib.utils import Utils

LOG=getLogger('m360.agents.tomcat')

APACHE_TOMCAT_COMMON_FORMAT="%h %l %u %t \"%r\" %s %b"
APACHE_TOMCAT_COMBINED_FORMAT="%h %l %u %t \"%r\" %s %b \"%{Referer}i\" \"%{User-Agent}i\""


class Instance (base.Instance):

    ALLOWED_MODULES = [Settings.HTTP,Settings.POOL,Settings.HEAP,Settings.THREADS,Settings.ACCESS,Settings.GC]

    def __init__(self,name,host,conf):
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self.data=None
        self._version=None
        self._jvmversion=None
        self._server_info=Manager.server_info(conf['endpoint'],conf['user'], conf['passwd'])
        if self._server_info:
            if u'Versión JVM' in self._server_info:
                self._jvmversion = self._server_info[u'Versión JVM']
            elif 'JVM Version' in self._server_info:
                self._jvmversion = self._server_info[u'JVM Version']
            else:
                self._jvmversion=conf['version']  if 'jvmversion' in conf else ""
            if u'Versión de Tomcat' in self._server_info:
                self._version = self._server_info[u'Versión de Tomcat']
            elif u'Tomcat Version' in self._server_info:
                self._version = self._server_info[u'Tomcat Version']
            else:
                self._version = conf['version'] if 'version' in conf else ""
        else:
            self._version=conf['version'] if 'version' in conf else ""
            self._jvmversion = conf['jvmversion'] if 'jvmversion' in conf else ""

    def getdata(self):
        if self.data == None:
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
            #Tomcat 5.0.x
            #Tomcat 8.x
            data = self.getdata()
            if 'JVM' in data:
                arrmetrics.append(data['JVM'])
            if 'MemoryPool' in data:
                arrmetrics.extend(data['MemoryPool'])
        except Exception as e:
            LOG.error("Error %s", str(e),extra={"monitor":self.tech,"modulo":"heap"})

        return arrmetrics

    def threads(self):
        arrmetrics=[]
        try:
            #Tomcat 5.0.x
            #Tomcat 8.x
            data = self.getdata()
            for tipo,metrics in data.iteritems():
                if tipo == 'JVM' or tipo == 'MemoryPool':
                    continue
                metrics['ConnectorName'] = tipo
                arrmetrics.append(metrics)
        except Exception as e:
            LOG.error("Error %s", str(e),extra={"monitor":self.tech,"modulo":"threads"})

        return arrmetrics

    def pool(self):
        data = []
        if self.version.find("5.0")>=0:
            pools = Manager.server_jmx(self.conf['endpoint'],
                                       self.conf['user'],
                                       self.conf['passwd'],
                                       rootnode="Catalina",
                                       beanname="DataSource",
                                       name="*")
        elif self.version.find("5.5") >= 0:
            pools = Manager.server_jmx(self.conf['endpoint'],
                                       self.conf['user'],
                                       self.conf['passwd'],
                                       rootnode="Catalina",
                                       beanname="DataSource",
                                       name="*")
        else:
            pools = Manager.server_jmx(self.conf['endpoint'],
                                            self.conf['user'],
                                            self.conf['passwd'],
                                            rootnode="tomcat.jdbc",
                                            beanname="ConnectionPool",
                                            name="*")

        for poolname,metrics in pools.iteritems():
            metrics['PoolName'] = poolname
            data.append(metrics)
        return data

    def access(self):
        data=Manager.getaccessmetrics(self)
        return data

    def http(self):
        data = []
        connectors = Manager.server_jmx(self.conf['endpoint'],
                                        self.conf['user'],
                                        self.conf['passwd'],
                                        beanname="GlobalRequestProcessor",
                                        name="*")

        for connectorname,metrics in connectors.iteritems():
            metrics['ConnectorName'] = connectorname
            data.append(metrics)
        return data

    def getlogfiles(self):
        CATALINA_HOME = self.conf['basepath']
        lognamepattern=None
        if not self._logfiles:
            logtuplatmp = {}
            self._logfiles = []
            acesslogBean = Manager.server_jmx(self.conf['endpoint'],
                                              self.conf['user'],
                                              self.conf['passwd'],
                                              metrics=False,
                                              beanname="Valve", host="localhost",
                                              name="AccessLogValve")
            tmpacesslogBean={}
            if 'AccessLogValve' in acesslogBean:
                ##TOMCAT 8: directoty,prefix,suffix,pattern,rotatable,fileDateFormat
                tmpacesslogBean=acesslogBean['AccessLogValve']
            if tmpacesslogBean:
                formato = APACHE_TOMCAT_COMMON_FORMAT
                if 'pattern' in tmpacesslogBean:
                    if tmpacesslogBean['pattern'].find("combined") >= 0:
                        formato = APACHE_TOMCAT_COMBINED_FORMAT
                    elif tmpacesslogBean['pattern'].find("common") >= 0:
                        formato = APACHE_TOMCAT_COMMON_FORMAT
                    elif tmpacesslogBean['pattern'] != "":
                        formato = tmpacesslogBean['pattern']
                fileDateFormat = tmpacesslogBean['fileDateFormat'].replace('yyyy','%Y').replace('MM','%m').replace('dd','%d')
                lognamepattern=os.path.join(CATALINA_HOME, tmpacesslogBean['directory'],
                                                       tmpacesslogBean['prefix'] +
                                                       fileDateFormat+
                                                       tmpacesslogBean['suffix'])
                logtuplatmp = {'host': 'localhost',
                                   'log': os.path.join(CATALINA_HOME, tmpacesslogBean['directory'],
                                                       tmpacesslogBean['prefix'] +
                                                       time.strftime(fileDateFormat,time.localtime()) +
                                                       tmpacesslogBean['suffix']),

                                   'format': formato}
            if logtuplatmp:
                self._logfiles=[]
                logtuplatmp['outputmetrics']=True
                logtuplatmp['lognamepattern'] = lognamepattern
                logtuplatmp['format']=Utils.parselogformat(logtuplatmp['format'])
                logtuplatmp['separator'] = Utils.logseparator(logtuplatmp['format'])
                logtuplatmp['keyposition']=Utils.keyposition(logtuplatmp['format'],logtuplatmp['separator'])
                #FICHERO ANTERIOR DE LOG ROTADO
                prevlog=Utils.previousRotateFile(lognamepattern,self)
                if prevlog:
                    #PRIMERO SIEMPRE EL LOG ANTERIOR
                    self._logfiles.append({'host':'localhost',
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
        return 1 if Manager.url_alive(self.conf['endpoint']) else 0
