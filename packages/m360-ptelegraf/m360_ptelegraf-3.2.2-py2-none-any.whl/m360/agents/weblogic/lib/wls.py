import wlsrestful12c
import wlsrestful11g
from m360.base.lib.utils import Utils
import os

DEFAULT_TIMEOUT = 3005

class WLSProxy(object):
    UNKNOWN_STATE = 1
    POOL_STATE = { "RUNNING": 0, "UNKNOWN":1, "OVERLOADED":2, "SUSPENDEND":3 , "SHUTDOWN": 4 }

    """
    Represents a abstract WLS REST server
    """
    def __init__(self,instanceObj, version='latest', verify=True,timeout=DEFAULT_TIMEOUT):
        urlbase=instanceObj.conf['endpoint']
        server=instanceObj.name
        username=instanceObj.conf['user']
        password=instanceObj.conf['passwd']
        self._isDomain=False if 'domain' in instanceObj.conf and instanceObj.conf['domain']==False else True
        self._cachejmx={}
        #Comprobamos la version de WL y retornamos el objeto que corresponda
        self._wls = None
        self._version = instanceObj.conf['version'] if 'version' in instanceObj.conf else ""
        self._runtime = None
        try:
            self._wls = wlsrestful12c.WLS(urlbase,username,password,version,verify,timeout)
            if self._isDomain:
                self._runtime = self._wls.domainRuntime.serverRuntimes.__getattr__(server.split("/")[-1])
                self._config  = self._wls.domainConfig
            else:
                self._runtime = self._wls.serverRuntime
                self._config  = self._wls.serverConfig

        except Exception as e:
            if not self._version.startswith("8"):
                self._wls = wlsrestful11g.WLS(urlbase, server, username, password, version, verify, timeout)

        if self._wls:
            self._version = self._wls.version

        self._wls8cmd = ""
        ##dependiendo de la version
        # /usr/local/jdk1.7.0_80/jre/bin/java -jar JBossJMXClient.jar 192.168.0.3 60299 jmxpro jmxPromonitor2015\! 58380 http
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if instanceObj.javaruntime:
            if self.version.find("10.3.") >= 0:
                jarname = "weblogicmonitor11g_JRE17.jar"
                lastpar = ""
                l_ip=urlbase.replace("http://","").replace("https://","").split(":")[0]
                l_port=urlbase.replace("http://","").replace("https://","").split(":")[1]
                cmd = instanceObj.javaruntime + " -jar " + path + "/jmxmonitor/"+jarname+" " + l_ip + " " + l_port + " " + username + " " + password + " " + server + " " + lastpar
                # returns output as byte string
                dataaux2 = Utils.runcmd(cmd,roottag="body",monitor="weblogic")
                if dataaux2['mensaje'] == "":  # HAY un bug en la clase y devuelve succcess (3 c)
                    self._cachejmx = dataaux2['body']['item']
            elif self.version.startswith("8"):
                java_home=instanceObj.conf['javaruntime'].replace("/bin/java","")
                wls_home=instanceObj.conf['wls_home']
                domain=instanceObj.conf['domain']
                self._wls8cmd = instanceObj.javaruntime + " -cp " + java_home+ "/lib/tools.jar:"+wls_home+\
                      "/server/lib/weblogic_sp.jar:" + wls_home + "/server/lib/weblogic.jar weblogic.Admin -url "+\
                      urlbase+" -username "+username+" -password "+password+" GET -pretty -mbean "+domain+\
                      ":ServerRuntime={0},Location={0},Name={1},Type={2}"
                cmd = instanceObj.javaruntime + " -cp " + java_home+ "/lib/tools.jar:"+wls_home+\
                      "/server/lib/weblogic_sp.jar:" + wls_home + "/server/lib/weblogic.jar weblogic.Admin -url "+\
                      urlbase+" -username "+username+" -password "+password+" GET -pretty -mbean "+domain+\
                      ":Location="+server+",Name="+server+",Type=ServerRuntime"
                # returns output as byte string
                dataaux2 = Utils.runcmd(cmd,roottag="body",monitor="weblogic",jsonmode=False)
                if dataaux2['mensaje'] == "":  # HAY un bug en la clase y devuelve succcess (3 c)
                    self._cachejmx = dataaux2['body']['item']


    @property
    def version(self):
        return self._version

    def getApplicationRuntimes(self,server):
        canonicalname=server.split("/")[-1]
        arrdata = []
        if self.version.find("10.3.")>=0:
            pass
        elif self.version.startswith("8"):
            pass
        else:
            ## Va por wls11g en "tenant-monitoring"
#            data=self._wls.get("applicationRuntimes")
            data = self._runtime.applicationRuntimes
            for app in data:
                if app['internal']:
                    continue
                l_data = {"name":app['name'],
                          "applicationName": app['applicationName'],
                          "type":app['type'],
                          "status": app['healthState']['state'],
                          "status_code": 1 if app['healthState']['state']=='ok' else 0
                }
                managerRuntimes = [app.workManagerRuntimes,app.managedExecutorServiceRuntimes,
                                   app.managedThreadFactoryRuntimes,app.managedScheduledExecutorServiceRuntimes]
                for managerRuntime in managerRuntimes:
                    for manager in managerRuntime:
                        for metric in dir(manager):
                            value = manager[metric]
                            if type(value) not in [float,int]:
                                continue
                            try:
                                l_data[metric]=l_data[metric]+value
                            except KeyError:
                                l_data[metric]=value
                runtimes = [app.classLoaderRuntime]
                for runtime in runtimes:
                    for metric in dir(runtime):
                        value = runtime[metric]
                        if type(value) not in [float, int]:
                            continue
                        try:
                            l_data[metric] = l_data[metric] + value
                        except KeyError:
                            l_data[metric] = value
                arrdata.append(l_data)
        return arrdata

    def getJVMRuntime(self,server):
        canonicalname=server.split("/")[-1]
        if self.version.find("10.3.")>=0:
            obj=self._wls.get("servers/"+canonicalname)
            data=obj['body']['item']
            data['heapFreePercent']=int((obj['body']['item']['heapFreeCurrent']*100)/obj['body']['item']['heapSizeCurrent']) if obj['body']['item']['heapSizeCurrent'] > 0  else 0
            return data
        elif self.version.startswith("8"):
            retdict={'heapSizeCurrent':"",'heapFreeCurrent':"",'heapSizeMax':"","heapFreePercent":""}
            dataaux2 = Utils.runcmd(self._wls8cmd.format(server,server,"JVMRuntime"),roottag="body",monitor="weblogic",jsonmode=False)
#        HeapFreeCurrent: 241195896
#        HeapSizeCurrent: 265486336
            if dataaux2['mensaje'] == "":  # HAY un bug en la clase y devuelve succcess (3 c)
                retdict['heapFreePercent']=int((int(dataaux2['body']['item']['HeapFreeCurrent'])*100)/int(dataaux2['body']['item']['HeapSizeCurrent'])) if int(dataaux2['body']['item']['HeapSizeCurrent']) > 0  else 0
                retdict['heapFreeCurrent']=int(dataaux2['body']['item']['HeapFreeCurrent'])
                retdict['heapSizeCurrent']=int(dataaux2['body']['item']['HeapSizeCurrent'])
                retdict['heapSizeMax']=int(dataaux2['body']['item']['HeapSizeCurrent'])
            return retdict
        else:
            return self._runtime.JVMRuntime

    def getThreadPoolRuntime(self,server):
        if self.version.find("10.3.")>=0:
            threaddata = self._cachejmx['runtime']['threadPoolRuntime']  if 'runtime' in self._cachejmx and 'threadPoolRuntime' in self._cachejmx['runtime'] else {}
            #Compatibilidad Weblogic12c
            threaddata['stuckThreadCount']=0
            return Utils.dict2namedtuple(threaddata,'threadPoolRuntime')
        elif self.version.startswith("8"):
            retdict={'executeThreadTotalCount':0,
                     'executeThreadIdleCount':0,
                     'hoggingThreadCount':0,
                     'standbyThreadCount':0,
                     'completedRequestCount':0,
                     'pendingRequestCurrentCount':0,
                     'queueLength':0,
                     'throughput':0,
                     "stuckThreadCount":0}
            dataaux2 = Utils.runcmd(self._wls8cmd.format(server,"weblogic.kernel.Default","ExecuteQueueRuntime"),roottag="body",monitor="weblogic",jsonmode=False)
            if dataaux2['mensaje'] == "":  # HAY un bug en la clase y devuelve succcess (3 c)
                retdict['executeThreadIdleCount']=dataaux2['body']['item']['ExecuteThreadCurrentIdleCount']
                retdict['executeThreadTotalCount']=dataaux2['body']['item']['ExecuteThreadTotalCount']
                retdict['pendingRequestCurrentCount']=dataaux2['body']['item']['PendingRequestCurrentCount']
                retdict['completedRequestCount']=dataaux2['body']['item']['ServicedRequestTotalCount']
            return Utils.dict2namedtuple(retdict,'threadPoolRuntime')
        else:
            return self._runtime.threadPoolRuntime


    def getChannels(self,server):
        if self.version.find("10.3.")>=0:
            return [Utils.dict2namedtuple(c,"channel") for c in self._cachejmx['runtime']['channelsRuntimes'] if 'runtime' in self._cachejmx and 'channelsRuntimes' in self._cachejmx['runtime']]
        elif self.version.startswith("8"):
            return []
        else:
            return self._runtime.serverChannelRuntimes

    def getJVMVersion(self,server):
        if self.version.find("10.3.")>=0:
            data=self._wls.get("servers/"+server.split("/")[-1])
            return data['body']['item']['javaVersion']
        elif self.version.startswith("8"):
            return ""
        else:
            return self._runtime.JVMRuntime.javaVersion

    def getJMSServers(self,server):
        arrdata=[]
        if self.version.find("10.3.")>=0:
            jmsdata =  self._cachejmx['runtime']['jmsservers'] if 'runtime' in self._cachejmx and 'jmsservers' in self._cachejmx['runtime'] else []
            for jms in jmsdata:
                if 'destinations' in jms and len(jms['destinations']) > 0:
                    for dest in jms['destinations']:
                        dest['name'] = jms['name']
                        arrdata.append(dest)
                else:
                    arrdata.append(jms)
                jms.pop('destinations', None)
        elif self.version.startswith("8"):
            return []
        else:
            jmsdata = self._runtime.JMSRuntime.JMSServers
            for jmsserver in jmsdata:
                l_name = jmsserver.name
                arrdata.append({"name":l_name,
                                "globalBytesCurrentCount":jmsserver.bytesCurrentCount,
                                "globalBytesHighCount":jmsserver.bytesHighCount,
                                "globalBytesPageableCurrentCount":jmsserver.bytesPageableCurrentCount,
                                "globalBytesPagedInTotalCount":jmsserver.bytesPagedInTotalCount,
                                "globalBytesPagedOutTotalCount":jmsserver.bytesPagedOutTotalCount,
                                "globalBytesPendingCount":jmsserver.bytesPendingCount,
                                "globalBytesReceivedCount":jmsserver.bytesReceivedCount,
                                "globalBytesThresholdTime":jmsserver.bytesThresholdTime,
                                "globalDestinationsCurrentCount":jmsserver.destinationsCurrentCount,
                                "globalDestinationsHighCount":jmsserver.destinationsHighCount,
                                "globalDestinationsTotalCount":jmsserver.destinationsTotalCount,
                                "globalMessagesCurrentCount":jmsserver.messagesCurrentCount,
                                "globalMessagesHighCount":jmsserver.messagesHighCount,
                                "globalMessagesPageableCurrentCount":jmsserver.messagesPageableCurrentCount,
                                "globalMessagesPagedInTotalCount":jmsserver.messagesPagedInTotalCount,
                                "globalMessagesPagedOutTotalCount":jmsserver.messagesPagedOutTotalCount,
                                "globalMessagesPendingCount":jmsserver.messagesPendingCount,
                                "globalMessagesReceivedCount":jmsserver.messagesReceivedCount,
                                "globalMessagesThresholdTime":jmsserver.messagesThresholdTime,
                                "globalSessionPoolsCurrentCount":jmsserver.sessionPoolsCurrentCount,
                                "globalSessionPoolsHighCount":jmsserver.sessionPoolsHighCount,
                                "globalSessionPoolsTotalCount":jmsserver.sessionPoolsTotalCount
                })
                if jmsserver.destinationsCurrentCount>0:
                    for dest in jmsserver.destinations:
                        arrdata.append({"name":l_name,"destination":dest.name,
                                        "destinationMessagesReceivedCount":dest.messagesReceivedCount,
                                        "destinationBytesHighCount":dest.bytesHighCount,
                                        "destinationBytesThresholdTime":dest.bytesThresholdTime,
                                        "destinationMessagesDeletedCurrentCount":dest.messagesDeletedCurrentCount,
                                        "destinationBytesReceivedCount":dest.bytesReceivedCount,
                                        "destinationMessagesHighCount":dest.messagesHighCount,
                                        "destinationConsumersTotalCount":dest.consumersTotalCount,
                                        "destinationMessagesThresholdTime":dest.messagesThresholdTime,
                                        "destinationBytesCurrentCount":dest.bytesCurrentCount,
                                        "destinationMessagesMovedCurrentCount":dest.messagesMovedCurrentCount,
                                        "destinationMessagesCurrentCount":dest.messagesCurrentCount,
                                        "destinationBytesPendingCount":dest.bytesPendingCount,
                                        "destinationMessagesPendingCount":dest.messagesPendingCount,
                                        "destinationConsumersCurrentCount":dest.consumersCurrentCount
                        })

        return arrdata

    def getDataSources(self,server):
        canonicalname=server.split("/")[-1]
        if self.version.find("10.3.")>=0:
            arrdata = []
            data=self._wls.get("datasources")

            for ds in data['body']['items']:
                dsname=ds['name']
                for ins in ds['instances']:
                    if canonicalname==ins['server']:
                        data2=self._wls.get("datasources/" + dsname)
                        for ins2 in data2['body']['item']['instances']:
                            if canonicalname==ins2['server']:
                                ins2['name']=dsname
                                ##ESTANDARIZACION CON WEBLOGIC12c
                                ins2['highestNumUnavailable']=-1
                                ins2['waitSecondsHighCount']=-1
                                tuple=Utils.dict2namedtuple(ins2,"datasource")
                                arrdata.append(tuple)
                                break
                        break

            return arrdata
        elif self.version.startswith("8"):
            return []
        else:
            return self._runtime.JDBCServiceRuntime.JDBCDataSourceRuntimeMBeans

    @staticmethod
    def convertState(statusStr):
        if statusStr:
            if statusStr.upper() in WLSProxy.POOL_STATE:
                return WLSProxy.POOL_STATE[statusStr.upper()]
            else:
                return WLSProxy.UNKNOWN_STATE
        else:
            return WLSProxy.UNKNOWN_STATE

    def getCurrentMachine(self,server):
        canonicalname=server.split("/")[-1]
        if self.version.find("10.3.")>=0:
            obj = self._wls.get("servers/" + canonicalname)
            return obj['body']['item']['currentMachine']
        elif self.version.startswith("8"):
            return ""
        else:
            return self._runtime.currentMachine

    def getHealth(self,server):
        if self.version.find("10.3.")>=0:
            data=self._wls.get("servers/"+server.split("/")[-1])
            return {'status':data['body']['item']['state'],'health':'unknown'}
        elif self.version.startswith("8"):
            return {'status':self._cachejmx['State'],'health':'unknown'}
        else:
            return {'status':self._runtime.state,'health':self._runtime.healthState['state']}

    def getState(self,server):
        if self.version.find("10.3.")>=0:
            data=self._wls.get("servers/"+server.split("/")[-1])
            return data['body']['item']['state']
        elif self.version.startswith("8"):
            return self._cachejmx['State']
        else:
            return self._runtime.state

    def getRootDirectory(self):
        if self.version.find("10.3.")>=0:
            return self._cachejmx['configuration']['rootDirectory'] if 'configuration' in self._cachejmx and 'rootDirectory' in self._cachejmx['configuration'] else ""
        elif self.version.startswith("8"):
            return ""
        else:
            return self._config.rootDirectory

    def getWebServerLog(self,server):
        if self.version.find("10.3.")>=0:
            return Utils.dict2namedtuple(self._cachejmx['configuration']['weblog'],"WebLog") if 'configuration' in self._cachejmx and 'weblog' in self._cachejmx['configuration'] else {}
        elif self.version.startswith("8"):
            return {}
        else:
            return self._config.servers.__getattr__(server.split("/")[-1]).webServer.webServerLog
