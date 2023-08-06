# coding=utf-8
import copy
from logging import getLogger
import re
import os
from m360.base.lib.utils import Utils
from m360.base.manager import Manager
from m360.base.settings import Settings
from m360.base.lib.psutilwrapper import stats

LOG = getLogger('m360.base')


class Instance(object):
    ALLOWED_TECHNOLOGIES = ["Weblogic","Jboss","Apache","Java","Tomcat","Mq","Linux","Windows","Tibco","Sqlserver","Control","Custom"]

    JVM_TECHS = ['tomcat','jboss','weblogic']
    JVM_VERSION_GCOPTIONS = { '1.8' : [ "-XX:+DisableExplicitGC",
                                        "-XX:+PrintGCDetails",
                                        "-XX:+PrintGCTimeStamps",
                                        "-XX:+PrintGCDateStamps",
                                        "-XX:+PrintGCApplicationStoppedTime",
                                        "-XX:+PrintTenuringDistribution",
                                        "-XX:+PrintHeapAtGC",
                                        "-verbose",
                                        "-XX:+UseG1GC", #G1
                                        "-XX:+UseParallelGC",
                                        "-XX:+UseParallelOldGC",
                                        "-XX:+UseSerialGC",
                                        "-XX:+UseConcMarkSweepGC", #CMS
                                        ]}

    #tecnologia de la instancia
    #configuracion de la instancia
    def __init__(self,tech,modules,name,host,conf):
        if not os.path.isdir(os.path.join(Settings.MONITOR_CACHE,tech)):
            os.mkdir(os.path.join(Settings.MONITOR_CACHE,tech), 0o777)

        if not os.path.isdir(os.path.join(Settings.MONITOR_CACHE,tech,'index')):
            os.mkdir(os.path.join(Settings.MONITOR_CACHE,tech,'index'), 0o777)

        MONITOR_TMPPATH = os.path.join(Settings.MONITOR_CACHE,tech,'tmp')
        if not os.path.isdir(os.path.join(Settings.MONITOR_CACHE,tech,'tmp')):
            os.mkdir(os.path.join(Settings.MONITOR_CACHE,tech,'tmp'), 0o777)

        self._indexpath = os.path.join(Settings.MONITOR_CACHE,tech,'index')
        self._modules = []
        if 'modules' in conf:
            for m in conf['modules']:
                if m.lower() in modules or tech=="custom":
                    self._modules.append(m.lower())
        else:
            self._modules = modules

        if tech in Settings.TECHNOLOGY_HEALTH:
            self._modules = self._modules + [Settings.HEALTH]

        self._tech = tech
        if tech in Instance.ALLOWED_TECHNOLOGIES:
            self._technology = tech
        elif "Technology" in conf:
            self._technology = conf["Technology"]
        else:
            self._technology = tech

        self._conf = conf
        self._name = name
        self._host = host
        self._starttime = 0
        self._state = 0 #0: Stopped, 1: Running ,2:Running with warning
        self._javaruntime = conf['javaruntime'] if 'javaruntime' in conf else None

        self._logfiles = []
        if 'vhosts' in conf and 'logformats' in conf:
            for vhost, tupla in conf['vhosts'].iteritems():
                aux_format=Utils.parselogformat(conf['logformats'][tupla['format']])
                sep = Utils.logseparator(aux_format)
                #incluimos el log anterior en hora o dia si no se ha terminado de procesar
                prevlog=Utils.previousRotateFile(tupla['log'],self)
                if prevlog:
                    #PRIMERO SIEMPRE EL LOG ANTERIOR
                    self._logfiles.append({'host':vhost,
                                           'lognamepattern':tupla['log'],
                                           'log':prevlog,
                                           'outputmetrics':False, #LAS METRICAS PROCESADAS DE UN LOG ANTERIOR NO SE ENVIAN
                                           'format': aux_format,
                                           'keyposition': Utils.keyposition(aux_format,sep),
                                           'separator': sep
                                           })
                self._logfiles.append({'host':vhost,
                                       'lognamepattern':tupla['log'],
                                       'log':Utils.convertDate(tupla['log']),
                                       'outputmetrics':True,
                                       'format': aux_format,
                                       'keyposition': Utils.keyposition(aux_format,sep),
                                       'separator': sep
                                       })

        self._outputs = []
        for name, conf in self._conf.items():
            if name.startswith("outputs."):
                self._outputs.append({name.split(".")[1]:conf})
        self.global_tags = {}
        if 'global_tags' in self._conf:
            self.global_tags = copy.deepcopy(self._conf['global_tags'])
        if "instance" not in self.global_tags:
            self.global_tags['instance'] = self.name
        if "host" not in self.global_tags:
            self.global_tags['host'] = self.host
        if "service" not in self.global_tags:
            self.global_tags['service'] = self._tech.capitalize()
        if "group" not in self.global_tags:
            self.global_tags['group'] = "INFRA"

        LOG.info("Instancia creada.",extra={'monitor':self.tech,'modulo':'none'})

    @property
    def version(self):
        if hasattr(self,"_version") and self._version:
            return self._version
        else:
            return "Unknown"

    @property
    def outputs(self):
        return self._outputs

    @property
    def javaruntime(self):
        return self._javaruntime

    @property
    def starttime(self):
        if self._starttime==0:
            pass
            #Obtenemos la hora de arranque de la instancia
        return self._starttime

    @property
    def technology(self):
        return self._technology

    @property
    def tech(self):
        return self._tech

    @property
    def host(self):
        return self._host

    @property
    def modules(self):
        return self._modules

    @property
    def name(self):
        return self._name

    @property
    def conf(self):
        return self._conf

    def users(self):
        raise NotImplementedError

    def app(self):
        raise NotImplementedError

    def tablespaces(self):
        raise NotImplementedError

    def sysstat(self):
        raise NotImplementedError

    def log(self):
        raise NotImplementedError

    def procstat(self):
        raise NotImplementedError

    def lookup(self):
        raise NotImplementedError

    def database(self):
        raise NotImplementedError

    def sessions(self):
        raise NotImplementedError

    def events(self):
        raise NotImplementedError

    def storage(self):
        raise NotImplementedError

    def asm(self):
        raise NotImplementedError

    def system(self):
        raise NotImplementedError

    def jms(self):
        raise NotImplementedError

    def heap(self):
        raise NotImplementedError

    def gc(self):
        if self._tech not in Instance.JVM_TECHS:
            raise NotImplementedError
        else:
            return Manager.getGCmetrics(self)

    def threads(self):
        raise NotImplementedError

    def oci_autonomous_database(self):
        raise NotImplementedError

    def access(self):
        raise NotImplementedError

    def pool(self):
        raise NotImplementedError

    def module(self):
        raise NotImplementedError

    def http(self):
        raise NotImplementedError

    def custom(self):
        raise NotImplementedError

    def getversion(self):
        return self.version

    def getjvmversion(self):
        raise NotImplementedError

    def getlogfiles(self):
        ##EL FORMATO YA ESTA EN EL LOG
        return self._logfiles


    def getgcfiles(self):
        if self._tech not in Instance.JVM_TECHS:
            raise NotImplementedError
        else:
            l_gclog = {'outputmetrics':True,'log':"",'format':'','host':"",'gcoptions':[]}
            ##COMPROBAMOS SI ESTA CONFIGURADO ANTES
            if 'gclog' in self.conf:
                l_gclog['log']=self.conf['gclog']
            else:
                ##BUSCAMOS LA VERSION DE JDK
                jvmversion = self.getjvmversion()
                l_majorver = Utils.majorversion(jvmversion)
                r = re.compile("\\b" + self.name + "\\b")
                #TODO: TIMESTAMP START PARA INCLUIR LA FECHA HORA SI ES RELATIVA
                jvms_ps = [p.info for p in stats.process_iter(attrs=['cmdline','name','pid']) if 'java' in p.info['name']]
                suffix=""
                for pinfo in jvms_ps:
                    newlist = [m for l in pinfo['cmdline'] for m in [r.search(l)] if m]
                    if len(newlist)>0:
                        p = stats.Process(pid=pinfo['pid'])
                        self._starttime = p.create_time()
                        ##BUSCAMOS LOS PARAMETROS DE GC
                        for par in pinfo['cmdline']:
                            if par in Instance.JVM_VERSION_GCOPTIONS[l_majorver]:
                                l_aux=par.split(":")
                                l_gclog['gcoptions'].append(l_aux[0] if l_aux[0].lower()=="verbose" else l_aux[1])

                            # -Xloggc: <filename>
                            gclog_search = re.search('-Xloggc:(.*)',par,re.IGNORECASE)
                            if gclog_search:
                                l_gclog['log'] = gclog_search.group(1).strip()
                            else:
                                # -Xlog:gc:<level>:file:<filename>
                                gclog_search = re.search('-Xlog:.*gc.*:file=([^:]+)', par, re.IGNORECASE)
                                if gclog_search:
                                    l_gclog['log'] = gclog_search.group(1).strip()

                            if par.find("UseGCLogFileRotation")>=0:
                                suffix=".0"
                        break
                if l_gclog['log']!="":
                    l_gclog['log']=l_gclog['log']+suffix

            return [l_gclog]


    def getindexpath(self):
        return self._indexpath

    def isrunning(self):
        return True

    def psmon(self):
        raise NotImplementedError

    def rcmon(self):
        raise NotImplementedError

    def webapplmon(self):
        raise NotImplementedError

    def cpu(self):
        raise NotImplementedError

    def net(self):
        raise NotImplementedError

    def disk(self):
        raise NotImplementedError

    def diskio(self):
        raise NotImplementedError

    def mem(self):
        raise NotImplementedError

    def swap(self):
        raise NotImplementedError

    def top(self):
        raise NotImplementedError

    def netstat(self):
        raise NotImplementedError

    def nstat(self):
        raise NotImplementedError

    def processes(self):
        raise NotImplementedError

    def health(self):
        return [{"status_code": 1 if self.isrunning() else 0}]

    def get_global_tags(self):
        return self.global_tags

    def agent(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    def memstats(self):
        raise NotImplementedError

    def gather(self):
        raise NotImplementedError
