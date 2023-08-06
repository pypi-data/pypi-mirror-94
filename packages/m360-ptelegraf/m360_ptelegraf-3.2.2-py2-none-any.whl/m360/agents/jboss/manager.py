# -*- coding: utf-8 -*-
import subprocess
import requests
import re
import m360.base.manager as base
from logging import getLogger
import xml.etree.ElementTree as ET
from m360.base.lib.utils import Utils
from requests.auth import HTTPDigestAuth
import json
import os
import urllib3
urllib3.disable_warnings()

LOG=getLogger('m360.agents.jboss')

class Manager(base.Manager):

    @staticmethod
    def server_jmx7EAP(status_url, username, password,**kargs):

        #Configuracion
        data = {}
        data['status'] = {}
        data['status']['connector'] = []
        data['status']['data-source'] = {}
        data['status']['logbean'] = {}
        args = {"operation": "read-resource","recursive":"true","address":[],
                "include-runtime": "true", "json.pretty": 1,"recusive-depth":10}
        try:
            LOG.debug("Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
            resp = requests.post(status_url,json=args,auth=HTTPDigestAuth(username,password),
                                 verify=False,timeout=10)
            resp.raise_for_status()
            dataaux = resp.json()
            LOG.debug("Requested: %s Res: %s", status_url,str(dataaux),extra={"monitor": "jboss", "modulo": "NA"})
            if dataaux['outcome']=="success":
                ##HEAP
                data['status']['jvm'] = {'memory': dataaux['result']['core-service']['platform-mbean']['type']['memory']['heap-memory-usage']}
                ##obtenemos el free
                data['status']['jvm']['memory']['free']=str(int(data['status']['jvm']['memory']['max'])-int(data['status']['jvm']['memory']['used']))
                data['status']['jvm']['memory']['total']=data['status']['jvm']['memory']['committed']
                data['status']['jvm']['memory'].pop('committed',None)

                #THREADS
                threadsInfo = { "currentThreadCount":dataaux['result']['core-service']['platform-mbean']['type']['threading']['thread-count'],
                                "ConnectionCreatedCount":dataaux['result']['core-service']['platform-mbean']['type']['threading']['total-started-thread-count'],
                                "currentDaemonThreadCount":dataaux['result']['core-service']['platform-mbean']['type']['threading']['daemon-thread-count'] }

                #CONECTORES
                if "web" in dataaux['result']['subsystem']:
                    LOG.warning("%s subsystem.web not implemented", status_url, extra={"monitor": "jboss", "modulo": "NA"})
                elif "undertow" in dataaux['result']['subsystem']:
                    if dataaux['result']['subsystem']['undertow']["server"]["default-server"]["ajp-listener"]:
                        connector=dataaux['result']['subsystem']['undertow']["server"]["default-server"]["ajp-listener"]
                        data['status']['connector'].append({ 'name': "ajp-listener",'requestInfo':{"bytesReceived":connector["default"]["bytes-received"],
                                                                                            "bytesSent":connector["default"]["bytes-sent"],
                                                                                            "errorCount":connector["default"]["error-count"],
                                                                                            "maxTime":connector["default"]["max-processing-time"],
                                                                                            "processingTime":connector["default"]["processing-time"],
                                                                                            "requestCount":connector["default"]["request-count"]},
                                                                                    'threadInfo':threadsInfo})
                    if dataaux['result']['subsystem']['undertow']["server"]["default-server"]["http-listener"]:
                        connector=dataaux['result']['subsystem']['undertow']["server"]["default-server"]["http-listener"]
                        data['status']['connector'].append({ 'name': "http-listener",'requestInfo':{"bytesReceived":connector["default"]["bytes-received"],
                                                                                            "bytesSent":connector["default"]["bytes-sent"],
                                                                                            "errorCount":connector["default"]["error-count"],
                                                                                            "maxTime":connector["default"]["max-processing-time"],
                                                                                            "processingTime":connector["default"]["processing-time"],
                                                                                            "requestCount":connector["default"]["request-count"]},
                                                                                    'threadInfo':threadsInfo})
                    if dataaux['result']['subsystem']['undertow']["server"]["default-server"]["https-listener"]:
                        connector=dataaux['result']['subsystem']['undertow']["server"]["default-server"]["https-listener"]
                        data['status']['connector'].append({ 'name': "https-listener",'requestInfo':{"bytesReceived":connector["https"]["bytes-received"],
                                                                                            "bytesSent":connector["https"]["bytes-sent"],
                                                                                            "errorCount":connector["https"]["error-count"],
                                                                                            "maxTime":connector["https"]["max-processing-time"],
                                                                                            "processingTime":connector["https"]["processing-time"],
                                                                                            "requestCount":connector["https"]["request-count"]},
                                                                                    'threadInfo':threadsInfo})
                    #LOG ACCESS
                    data['status']['logbean']=dataaux['result']['subsystem']['undertow']["server"]["default-server"]['host']['default-host']['setting']['access-log']
                    data['status']['logbean']['log-dir']=dataaux['result']['core-service']['server-environment']['log-dir']

                else:
                    LOG.error("%s subsystem.web or subsystem.undertow not found", status_url, extra={"monitor": "jboss", "modulo": "NA"})

                #POOL
                if "data-source" in dataaux['result']['subsystem']['datasources'] and dataaux['result']['subsystem']['datasources']['data-source']:
                    data['status']['data-source'] = dataaux['result']['subsystem']['datasources']['data-source']


        except Exception as e:
            LOG.error("Request: %s ERRMSG: %s", status_url, e.message, extra={"monitor": "jboss", "modulo": "http"})

        return data

    @staticmethod
    def server_jmx(status_url, username, password,**kargs):

        if 'access' in kargs and kargs['access']:
            ret = {}
            path = os.path.dirname(os.path.abspath(__file__))
            cmd = kargs['java'] + " -jar " + path + "/jmxmonitor/JBossJMXClient"+kargs['majorversion']+".jar " + kargs['ip'] + " " + kargs['jmxport'] + " " + " " + username + " " + password+" "+kargs['beanname']
            LOG.debug("Executing: %s", cmd, extra={"monitor": "jboss", "modulo": "access"})
            # returns output as byte string
            try:
#                returned_output = subprocess.check_output(cmd.split(),stderr=subprocess.PIPE)
                returned_output = subprocess.check_output(cmd.split(),stderr=subprocess.STDOUT,universal_newlines=True)
                dataaux2 = json.loads(Utils.grep(returned_output,"outcome"))
                if dataaux2['outcome'] == "success":  # HAY un bug en la clase y devuelve succcess (3 c)
                    ret = dataaux2['result']
            except subprocess.CalledProcessError as e:
                LOG.error("Executed: %s ERRCODE: %s ERRMSG: %s",cmd,e.returncode,Utils.grep(e.output,"exception"), extra={"monitor": "jboss", "modulo": "access"})
            except Exception as e:
                LOG.error("Executed: %s ERRMSG: %s",cmd,e.message, extra={"monitor": "jboss", "modulo": "access"})
            LOG.debug("Executed: %s", cmd, extra={"monitor": "jboss", "modulo": "access"})
            return ret

        if 'pool' in kargs and kargs['pool']:
            ret = {}
            path = os.path.dirname(os.path.abspath(__file__))
            cmd = kargs['java'] + " -jar " + path + "/jmxmonitor/JBossJMXClient"+kargs['majorversion']+".jar " + kargs['ip'] + " " + kargs['jmxport'] + " " + " " + username + " " + password
            # returns output as byte string
            LOG.debug("Executing: %s", cmd, extra={"monitor": "jboss", "modulo": "pool"})
            try:
                #returned_output = subprocess.check_output(cmd.split(),stderr=subprocess.PIPE)
                returned_output = subprocess.check_output(cmd.split(),stderr=subprocess.STDOUT, universal_newlines=True)
                dataaux2 = json.loads(Utils.grep(returned_output,"outcome"))
                if dataaux2['outcome'] == "success":
                    retaux = {}
                    for ds,metrics in dataaux2['result'].iteritems():
                        retaux[ds] = { 'statistics': {'pool' : metrics  }}
                    ret['data-source'] = retaux
            except subprocess.CalledProcessError as e:
                LOG.error("Executed: %s ERRCODE: %s ERRMSG: %s",cmd,e.returncode,Utils.grep(e.output,"exception"), extra={"monitor": "jboss", "modulo": "pool"})
            except Exception as e:
                LOG.error("Executed: %s ERRMSG: %s",cmd,e.message, extra={"monitor": "jboss", "modulo": "pool"})
            LOG.debug("Executed: %s", cmd, extra={"monitor": "jboss", "modulo": "pool"})
            return ret

        if 'beanname' in kargs:
            ret = {}
            args = {"operation": "read-resource", "include-runtime": "true", "json.pretty": 1}
            #args["address"] = [{"core-service": "platform-mbean"}, {"type": "runtime"}]
            args['address'] = [{res.split("=")[0]:res.split("=")[1]} for res in kargs['beanname'][1:].split("/")]
            if 'recursive' in kargs:
                args["recursive"] = kargs['recursive']

            try:
                LOG.debug("Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
                resp = requests.post(status_url, json=args, auth=HTTPDigestAuth(username, password),verify=False,timeout=1)
                resp.raise_for_status()
                dataaux = resp.json()
                LOG.debug("Requested: %s Res: %s", status_url,str(dataaux),extra={"monitor": "jboss", "modulo": "NA"})
                if dataaux['outcome'] == "success":
                    ret = dataaux['result']
            except Exception as e:
                LOG.error("Request: %s ERRMSG: %s",status_url,e.message, extra={"monitor": "jboss", "modulo": "http"})
            return ret

        #Configuracion
        args = {"operation": "read-attribute", "include-runtime": "true", "json.pretty": 1}
        args["address"] = [{"core-service":"platform-mbean"},{"type":"runtime"}]
        args['name'] = "system-properties"
        try:
            LOG.debug("Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
            resp = requests.post(status_url,json=args,auth=HTTPDigestAuth(username,password),
                                 verify=False,timeout=5)
            resp.raise_for_status()
            dataaux = resp.json()
            LOG.debug("Requested: %s Res: %s", status_url,str(dataaux),extra={"monitor": "jboss", "modulo": "NA"})
            if dataaux['outcome']=="success":
                java=dataaux['result']['java.home']+"/bin/java"
                args["operation"]="read-resource"
                args["address"] = [{"socket-binding-group":"standard-sockets"},{"socket-binding":"management-native"}]
                LOG.debug("Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
                resp = requests.post(status_url,json=args,auth=HTTPDigestAuth(username,password),
                                     verify=False,timeout=5)
                resp.raise_for_status()
                dataaux = resp.json()
                LOG.debug("Requested: %s Res: %s", status_url,str(dataaux),extra={"monitor": "jboss", "modulo": "NA"})
                if dataaux['outcome']=="success":
                    ipmanagement=dataaux['result']['bound-address']
                    jmxport=str(dataaux['result']['bound-port'])

        except Exception as e:
            LOG.error("Request: %s ERRMSG: %s", status_url, e.message, extra={"monitor": "jboss", "modulo": "http"})

        data = {}
        data['status'] = {}
        data['status']['connector'] = []
        args={"operation":"read-resource","include-runtime":"true","json.pretty":1}
        #PRIMERO LA HEAP
        args["address"] = [{"core-service":"platform-mbean"},{"type":"memory"}]
        try:
            LOG.debug("Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
            resp = requests.post(status_url,json=args,auth=HTTPDigestAuth(username,password),
                                 verify=False,timeout=5)
            resp.raise_for_status()
        except Exception as e:
            return data
        if resp.status_code==200:
            dataaux = resp.json()
            LOG.debug("Requested: %s Res: %s", status_url,str(dataaux),extra={"monitor": "jboss", "modulo": "NA"})
            if dataaux['outcome']=="success":
                data['status']['jvm'] = {'memory': dataaux['result']['heap-memory-usage']}
                ##obtenemos el free
                data['status']['jvm']['memory']['free']=str(int(data['status']['jvm']['memory']['max'])-int(data['status']['jvm']['memory']['used']))
                data['status']['jvm']['memory']['total']=data['status']['jvm']['memory']['committed']
                data['status']['jvm']['memory'].pop('committed',None)

        #CONNECTORES
        args["address"] = [{"subsystem":"web"}]
        #subsystem= web: read-children-names(child-type=connector)
        args["operation"]="read-children-names"
        args["child-type"]="connector"
        args["recursive"] = "false"
        try:
            LOG.debug("Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
            resp = requests.post(status_url,json=args,auth=HTTPDigestAuth(username,password),
                                 verify=False,timeout=5)
            resp.raise_for_status()
        except Exception as e:
            return data
        if resp.status_code==200:
            dataaux = resp.json()
            LOG.debug("Requested: %s Res: %s", status_url,str(dataaux),extra={"monitor": "jboss", "modulo": "NA"})
            if dataaux['outcome']=="success":
                for connector in dataaux['result']:
                    args={"address":[{"subsystem":"web"},{"connector":str(connector)}],"operation":"read-resource",
                          "include-runtime": "true", "json.pretty": 1,"recursive":"true"}
                    try:
                        LOG.debug("Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
                        resp = requests.post(status_url,json=args,auth=HTTPDigestAuth(username,password),
                                             verify=False,timeout=5)
                        resp.raise_for_status()
                    except Exception as e:
                        LOG.error("ERROR Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
                        continue
                    #THREADS
                    if resp.status_code==200:
                        dataaux4 = resp.json()
                        threadsInfo = {}
                        if java and ipmanagement and jmxport:
                            #OBTENEMOS EL PUERTO:
                            args["operation"] = "read-resource"
                            args["address"] = [{"socket-binding-group": "standard-sockets"},
                                               {"socket-binding": dataaux4['result']['socket-binding']}]
                            LOG.debug("Requesting: %s Pars: %s", status_url,str(args),extra={"monitor": "jboss", "modulo": "NA"})
                            resp = requests.post(status_url, json=args, auth=HTTPDigestAuth(username, password),
                                                 verify=False,timeout=5)
                            resp.raise_for_status()
                            dataaux3 = resp.json()
                            LOG.debug("Requested: %s Res: %s", status_url,str(dataaux3),extra={"monitor": "jboss", "modulo": "NA"})
                            if dataaux3['outcome'] == "success":
                                ip = dataaux3['result']['bound-address']
                                port = str(dataaux3['result']['bound-port'])

                            #/usr/local/jdk1.7.0_80/jre/bin/java -jar JBossJMXClient.jar 192.168.0.3 60299 jmxpro jmxPromonitor2015\! 58380 http
                            path=os.path.dirname(os.path.abspath(__file__))
                            cmd=java+" -jar "+path+"/jmxmonitor/JBossJMXClient6_"+kargs['majorversion']+".jar "+ipmanagement+" "+jmxport+" "+" "+username+" "+password+" "+port+" "+connector[0]
                            # returns output as byte string
                            try:
                                returned_output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT,universal_newlines=True)
                                dataaux2 = json.loads(Utils.grep(returned_output, "outcome"))
                                if dataaux2['outcome'] == "succcess": #HAY un bug en la clase y devuelve succcess (3 c)
                                    threadsInfo = dataaux2['result']
                            except subprocess.CalledProcessError as e:
                                LOG.error("Executed: %s ERRCODE: %s ERRMSG: %s", cmd, e.returncode,Utils.grep(e.output, "exception"),extra={"monitor": "jboss", "modulo": "pool"})
                            except Exception as e:
                                LOG.error("Error %s", e.message, extra={"monitor": "jboss", "modulo": "threads"})

                        ##obtenemos el free
                        data['status']['connector'].append({ 'name': str(connector),
                                                             'requestInfo':{"bytesReceived":dataaux4['result']["bytesReceived"],
                                                                            "bytesSent":dataaux4['result']["bytesSent"],
                                                                            "errorCount":dataaux4['result']["errorCount"],
                                                                            "maxTime":dataaux4['result']["maxTime"],
                                                                            "processingTime":dataaux4['result']["processingTime"],
                                                                            "requestCount":dataaux4['result']["requestCount"]},
                                                             'threadInfo':threadsInfo})

        return data

    @staticmethod
    def server_status(status_url, username, password):
        resp = requests.get(status_url+"?XML=true", auth=(username, password),
                            timeout=1,verify=False)
        resp.raise_for_status()

        #scrape the HTML

        rootxmldoc = ET.fromstring(resp.text)
        #<jvm ><memory free='1627250776' total='2147483648' max='2147483648'/></jvm>
        res = Utils.etree_to_dict(rootxmldoc)
        return res

    @staticmethod
    def to_bytes(value):
        ret2 = 0
        ret = value.replace(' ','')
        ret = re.sub("\(.*\)","",ret)
        if re.search("[0-9](MB|KB|GB|B)$",ret):
            factor = 1
            if ret.endswith("MB"):
                factor = 1024 * 1024
            elif ret.endswith("KB"):
                factor = 1024
            elif ret.endswith("GB"):
                factor = 1024 * 1024 * 1024

            try:
                ret = float(re.sub("[A-Za-z]","",ret))*factor
            except Exception as e:
                return ret

        return ret
