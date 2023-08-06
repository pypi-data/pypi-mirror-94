# -*- coding: utf-8 -*-
import json
import os
import urllib2

import m360.base.manager as base
from logging import getLogger
from m360.agents.weblogic.lib.wls import WLSProxy

LOG=getLogger('m360.agents.weblogic')

class Manager(base.Manager):

    def __init__(self,instance):
        self._wls = None
        try:
            self._wls = WLSProxy(instance, 'latest', verify=False,timeout=60)
        except Exception as e:
            LOG.error("[%s] Error conectando con el Endpoint. Error: %s",instance.name,e.message,extra=self.getcaller())
        self._instance = instance

    def getWLSversion(self):
        version = self._instance.conf['version'] if 'version' in self._instance.conf else None
        if self._wls is None:
            return version
        try:
            version = self._wls.version
        except Exception as e:
            LOG.error("[%s] Error obteniendo la version JVM. Error: %s",self._instance.name,e.message,extra=self.getcaller())
        return version

    def getjvmversion(self):
        version = None
        if self._wls is None:
            return version
        try:
            version = self._wls.getJVMVersion(self._instance.name)
        except Exception as e:
            LOG.error("[%s] Error obteniendo la version JVM Error: %s",self._instance.name,e.message,extra=self.getcaller())
        return version

    def getheapdata(self):
        data = []
        if self._wls is None:
            return data
        try:
            obj = self._wls.getJVMRuntime(self._instance.name)
            data.append({'current':obj['heapSizeCurrent'],'free':obj['heapFreeCurrent'],'max':obj['heapSizeMax'],"freeprc":obj['heapFreePercent']})
        except Exception as e:
            LOG.error("[%s] Error obteniendo metricas. Error: %s",self._instance.name,e.message,extra=Manager.getcaller())

        return data


    def getchannelsdata(self):
        data = []
        if self._wls is None:
            return data
        try:
            channels = self._wls.getChannels(self._instance.name)
            for channel in channels:
                channelName = channel.name
                if channelName.find("http") != -1:
                    data.append({"name":channelName,
                                "msg_received":channel.messagesReceivedCount,
                                "connections":channel.connectionsCount,
                                "msg_sent":channel.messagesSentCount,
                                "bytes_received":channel.bytesReceivedCount,
                                "connections_accepted":channel.acceptCount ,
                                "bytes_sent": channel.bytesSentCount})
        except Exception as e:
            LOG.error("[%s] Error obteniendo metricas. Error: %s",self._instance.name,e.message,extra=Manager.getcaller())

        return data

    def getthreadsdata(self):
        data = []
        if self._wls is None:
            return data
        try:
            threadpool = self._wls.getThreadPoolRuntime(self._instance.name)
            active = int(threadpool.executeThreadTotalCount)
            idle = int(threadpool.executeThreadIdleCount)
            hogging = int(threadpool.hoggingThreadCount)
            standby = int(threadpool.standbyThreadCount)
            stuck = int(threadpool.stuckThreadCount)
#            stateBean = threadpool.healthState
            busy = int(active - idle - stuck - hogging)
            total = int(active + standby)
            maxthread = 1200

            data.append({   "active":active,
                            "busy":busy,
                            "iddle":idle,
                            "hogging":hogging,
                            "stuck":stuck,
                            "stadby":standby,
                            "max": maxthread,
                            "pendingRequestCount":threadpool.pendingRequestCurrentCount if hasattr(threadpool, 'pendingRequestCurrentCount') else 0, #WL8.1
                            "completedRequestCount":threadpool.completedRequestCount,
                            "queueLength":threadpool.queueLength,
                            "throughput":float(threadpool.throughput)
#                            "state":stateBean['state']
                         })

        except Exception as e:
            LOG.error("[%s] Error obteniendo metricas. Error: %s",self._instance.name,e.message,extra=Manager.getcaller())

        return data

    def getjmsdata(self):
        data = []
        if self._wls is None:
            return data
        try:
            data = self._wls.getJMSServers(self._instance.name)
        except Exception as e:
            LOG.error("[%s] Error obteniendo metricas. Error: %s",self._instance.name,e.message,extra=Manager.getcaller())
        return data

    def getapps(self):
        data = []
        if self._instance.name != "AdminServer":
            if self._wls is None:
                return data
            return self._wls.getApplicationRuntimes(self._instance.name)
        return data

    def getdatabasepoolsdata(self):
        data = []
        if self._wls is None:
            return data
        try:
            JDBCpools = self._wls.getDataSources(self._instance.name)
            for dataSource in JDBCpools:
                data.append({
                        "PoolName": dataSource.name,
                        "ActiveConnectionsAverageCount": dataSource.activeConnectionsAverageCount,
                        "ActiveConnectionsCurrentCount": dataSource.activeConnectionsCurrentCount,
                        "ActiveConnectionsHighCount": dataSource.activeConnectionsHighCount,
                        "ConnectionDelayTime": dataSource.connectionDelayTime,
                        "ConnectionsTotalCount": dataSource.connectionsTotalCount,
                        "CurrCapacity": dataSource.currCapacity,
                        "CurrCapacityHighCount": dataSource.currCapacityHighCount,
                        "FailedReserveRequestCount": dataSource.failedReserveRequestCount,
                        "FailuresToReconnectCount": dataSource.failuresToReconnectCount,
                        "HighestNumAvailable": dataSource.highestNumAvailable,
                        "HighestNumUnavailable": dataSource.highestNumUnavailable,
                        "LeakedConnectionCount": dataSource.leakedConnectionCount,
                        "NumAvailable": dataSource.numAvailable,
                        "NumUnavailable": dataSource.numUnavailable,
                        "PrepStmtCacheAccessCount": dataSource.prepStmtCacheAccessCount,
                        "PrepStmtCacheAddCount": dataSource.prepStmtCacheAddCount,
                        "PrepStmtCacheCurrentSize": dataSource.prepStmtCacheCurrentSize,
                        "PrepStmtCacheDeleteCount": dataSource.prepStmtCacheDeleteCount,
                        "PrepStmtCacheHitCount": dataSource.prepStmtCacheHitCount,
                        "PrepStmtCacheMissCount": dataSource.prepStmtCacheMissCount,
                        "ReserveRequestCount": dataSource.reserveRequestCount,
                        "State": WLSProxy.convertState(dataSource.state),
                        "WaitingForConnectionCurrentCount": dataSource.waitingForConnectionCurrentCount,
                        "WaitingForConnectionFailureTotal": dataSource.waitingForConnectionFailureTotal,
                        "WaitingForConnectionHighCount": dataSource.waitingForConnectionHighCount,
                        "WaitingForConnectionSuccessTotal": dataSource.waitingForConnectionSuccessTotal,
                        "WaitingForConnectionTotal": dataSource.waitingForConnectionTotal,
                        "WaitSecondsHighCount": dataSource.waitSecondsHighCount
                })
        except Exception as e:
            LOG.error("[%s] Error obteniendo metricas. Error: %s",self._instance.name,e.message,extra=Manager.getcaller())

        return data


    def getlogfiles(self):
        logfile = []
        if self._wls is None:
            return logfile

        if self.getWLSversion().startswith("8"):
            return  logfile

        if (self._wls.getState(self._instance.name) != "RUNNING"):
            return logfile

        domainPath = self._wls.getRootDirectory()
        httpLogMB = self._wls.getWebServerLog(self._instance.name)

        ##SI ESTA HABILITADO EL LOG DE ACCESOS
        logenabled=True

        ##BUG DESCONOCIDO WEBLOGIC
        try:
            logenabled = httpLogMB.loggingEnabled
        except Exception as e:
            pass

        if logenabled:
            serverPath = os.path.join(domainPath,'servers',self._instance.name)
            filenameLog = httpLogMB.fileName
            formatLog = httpLogMB.logFileFormat

            if formatLog == "extended":
                fieldsLog = httpLogMB.ELFFields
            else:
                fieldsLog = "date time cs-method cs-uri sc-status"

           #TODO: COMPROBAR ROTADO Y SI ROTA POR NUMERO DE FICHERO
            if not filenameLog.startswith('/'):
                filenameLog = os.path.join(serverPath,filenameLog)

            logfile.append({'filename':filenameLog,'format':fieldsLog})
        return logfile

    def getstate(self):
        l_state = "UNKNOWN"
        if self._wls is None:
            return l_state

        try:
            l_state = self._wls.getState(self._instance.name)
        except Exception as e:
            LOG.error("[%s] Error obteniendo estado instacia. Error: %s",self._instance.name,e.message,extra=Manager.getcaller())
        return l_state

    def gethealth(self):
        ret = { 'status':"UNKNOWN", 'health':"UNKNOWN"}
        if self._wls is None:
            return ret
        try:
            ret = self._wls.getHealth(self._instance.name)
        except Exception as e:
            LOG.error("[%s] Error obteniendo estado instacia. Error: %s",self._instance.name,e.message,extra=Manager.getcaller())
        return ret

    def gethost(self):
        l_host = None
        if self._wls is None:
            return l_host

        try:
            l_host = self._wls.getCurrentMachine(self._instance.name)
        except Exception as e:
            LOG.error("[%s] Error obteniendo host de la instacia. Error: %s",self._instance.name,e.message,extra=Manager.getcaller())
        return None if l_host=="" else l_host

    def tenant(self,uri):
        baseURL = "http://%s:%s/management/tenant-monitoring/servers" % (host, port)

        # HTTP Authentication
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, baseURL, username, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

        try:
            req = urllib2.Request(baseURL, None, {'Accept': 'application/json'})
            raw = urllib2.urlopen(req).read()
            data = json.loads(raw)
            items = data['body']['items']

            for item in items:
                print "Server: " + item['name'] + " [ " + item['state'] + " ]"

        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code

        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
        return