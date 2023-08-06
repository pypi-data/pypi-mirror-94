import base64
import datetime
import fnmatch
import hashlib
import os
import random
import urllib3
import time
from logging import getLogger
import requests
from requests.exceptions import HTTPError
import socket

from m360.base.lib.utils import Utils
from m360.base.telegraf_compat import get_tag_compat,get_field_compat,get_measurement_compat
import m360.base.settings as base
from m360.base.output import OutputBase
from m360.base.models import Timeseries

urllib3.disable_warnings()
LOG = getLogger('m360.outputs.influxdb')


class Output(OutputBase):
    def __init__(self,instance,conf=None):
        super(Output,self).__init__(instance,conf=conf)
        self._buffer = {}

    @property
    def agent(self):
        return type(self.conf) is dict and self.conf

    @property
    def write_consistency(self):
        ##DEVOLVEMOS UNA URL DEL POOL
        if self.agent and 'write_consistency' in self.conf:
            return self.conf['write_consistency']
        return "any"

    @property
    def urls(self):
        ##DEVOLVEMOS UNA URL DEL POOL
        if self.agent and 'urls' in self.conf:
            return self.conf['urls']
        return []

    @property
    def url(self):
        if self.write_consistency == "any":
            ret = [ random.choice(self.conf['urls']) ]
        elif self.write_consistency == "all":
            ret = self.conf['urls']
        else:
            ret =  []

        return [ "{0}/write?db={1}&rp={2}&u={3}&p={4}&precision=ns".format(url,
                                                                      self.database,
                                                                      self.retention_policy,
                                                                      self.username,
                                                                      self.passwd)
                 for url in ret ]

    @property
    def timeout(self):
        if self.agent and 'timeout' in self.conf:
            return self.conf['timeout']
        return 5.0

    @property
    def verify(self):
        if self.agent and 'insecure_skip_verify' in self.conf:
            return self.conf['insecure_skip_verify']
        return True

    @property
    def passwd(self):
        if self.agent and 'password' in self.conf:
            return self.conf['password']
        return ""

    @property
    def retention_policy(self):
        if self.agent and 'retention_policy' in self.conf:
            return self.conf['retention_policy']
        return "autogen"

    @property
    def skip_database_creation(self):
        if self.agent and 'skip_database_creation' in self.conf:
            return self.conf['skip_database_creation']
        return True

    @property
    def database(self):
        if self.agent and 'database' in self.conf:
            return self.conf['database']
        return "telegraf"

    @property
    def tech(self):
        return self.instance.technology

    @property
    def username(self):
        if self.agent and 'username' in self.conf:
            return self.conf['username']
        return ""

    @property
    def buffersize(self):
        if self.agent and 'BUFFERSIZE' in self.conf:
            return self.conf['BUFFERSIZE']
        return ""

    def write(self,host,modulo,metricasobj):
        _formatted_metrics = self.get_formatted_metrics(host,modulo,metricasobj)
        if _formatted_metrics:
            now=datetime.datetime.now()
            filename=self.instance.technology.lower()+"_"+modulo.lower()+"_"+host.upper()+"_"+self.instance.name.replace("/","")\
                .replace("_","")+"."+now.strftime("%Y-%m-%d")
            l_date = now.strftime("%Y-%m-%d")
            self._post(host, modulo, l_date, _formatted_metrics, filename)
        self._sendBufferAgent()

    def _addToBuffer(self, data):
        hash = hashlib.md5(
            data['header']['host'] + data['header']['instance'] + data['header']['modulo'] + data['header']['date'] +
            data['header']['filename'] + data['header']['technology']
        ).hexdigest()
        if hash not in self._buffer:
            self._buffer[hash] = {'header': data['header'], 'body': []}
        self._buffer[hash]['body'].extend(data['body'])
        if len(self._buffer[hash]['body']) >= self.buffersize:
            self._sendBufferAgent()

    def _post(self, host, modulo, date, metricastr, filename):
        ##TODO: USAMOS BUFFER
        jsdata = {}
        jsdata['header'] = {"host": host, "instance": self.instance.name, "modulo": modulo, "date": date,
                            "filename": filename, "technology": self.instance.technology.lower()}
        jsdata['body'] = metricastr
        self._addToBuffer(jsdata)

    def _send(self,data):
        res = {}
        for url in self.url:
            try:
                headers={
                    "Content-Type": "text/plain; charset=utf-8"
                }
                verify = "insecure_skip_verify" in self.conf and self.conf['insecure_skip_verify']
                timeout=5
                if "timeout" in self.conf:
                    timeout=Utils.convert_interval(self.conf['timeout'])
                response = requests.post(url,
                                         headers=headers,
                                         data="\n".join(data['body'])+"\n",
                                         verify=verify,
                                         timeout=timeout)
                if response.status_code == 204:
                    res['lines']=len(data['body'])
                else:
                    raise HTTPError(response.status_code)
            except Exception as e:
                LOG.error("Cannot send data to %s. HTTP error: %s", url, str(e),
                          extra={'monitor': self.tech, 'modulo': "NA"})

        return res

    def _sendCacheAgent(self):
        ##Buscamo el fichero de cache de la tech y dia hoy y ayer
        filename = hashlib.md5(self.instance.host + self.tech).hexdigest()
        hoy = datetime.datetime.now()
        currentdate = hoy - datetime.timedelta(days=base.Settings.RETENTION)
        matches = []
        for root, dirnames, filenames in os.walk(base.Settings.AGENT_CACHE):
            while currentdate <= hoy:
                for filename in fnmatch.filter(filenames, filename + "." + currentdate.strftime("%Y-%m-%d")):
                    matches.append(os.path.join(root, filename))
                currentdate = currentdate + datetime.timedelta(days=1)

        for filename in matches:
            linesnotsent = []
            linestosend = []
            prev = ""
            linecount = 0
            bodyarr = []
            head = {}
            lines = 0
            with open(filename, 'r') as f:
                for line in f:
                    lines = lines + 1
                    splitted = line.replace("\n", "").split(" ")
                    newhead = splitted[0:6]
                    newbody = splitted[6:]
                    now = " ".join(newhead)
                    if linecount >= self.buffersize or (now != prev and prev):
                        ret = self._send({"header": head, "body": bodyarr})
                        if 'lines' in ret and (ret['lines'] == len(bodyarr) or ret['lines'] == -1):
                            LOG.info("Metricas en cache enviadas correctamente al agente. Series: %s",
                                     str(ret['lines']),
                                     extra={'monitor': head['technology'], 'modulo': head['modulo']})
                        else:
                            LOG.warning("Metricas en cache NO enviadas correctamente al agente. Series: %s",str(len(bodyarr)),
                                        extra={'monitor': head['technology'], 'modulo': head['modulo']})
                            linesnotsent.extend(linestosend)
                        linecount = 0
                        bodyarr = []
                        linestosend = []

                    bodyarr.append(" ".join(newbody))
                    linestosend.append(line)
                    linecount = linecount + 1
                    head = {"host": splitted[0], "instance": splitted[1], "modulo": splitted[2], "date": splitted[3],
                            "filename": splitted[4], "technology": splitted[5]}
                    prev = now

                if bodyarr:
                    ret = self._send({"header": head, "body": bodyarr})
                    if 'lines' in ret and (ret['lines'] == len(bodyarr) or ret['lines'] == -1):
                        LOG.info("Metricas en cache enviadas correctamente al agente. Series: %s",
                                 str(ret['lines']), extra={'monitor': head['technology'],
                                                           'modulo': head['modulo']})
                    else:
                        linesnotsent.extend(linestosend)

            if linesnotsent:
                if len(linesnotsent) != lines:
                    with open(filename, 'w') as f:
                        f.writelines(linesnotsent)
            else:
                os.remove(filename)

    def _addToCache(self,data):
        if not os.path.isdir(base.Settings.MONITOR_CACHE):
            os.mkdir(base.Settings.MONITOR_CACHE)
        if not os.path.isdir(base.Settings.AGENT_CACHE):
            os.mkdir(base.Settings.AGENT_CACHE)
        hash = hashlib.md5(data['header']['host'] + self.tech).hexdigest()
        #        hash = hashlib.md5(data['header']['host'] + data['header']['instance'] + data['header']['modulo'] + data['header']['date'] + data['header']['filename'] + self.tech).hexdigest()
        #        hash=hashlib.md5(url).hexdigest()
        filename = os.path.join(base.Settings.AGENT_CACHE, hash + "." + data['header']['date'])
        filesize = 0L
        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)

        if filesize < base.Settings.AGENT_CACHEMAXSIZE:
            linearray = []
            with open(filename, 'a') as f:
                for line in data['body']:
                    linearray.append(data['header']['host'] + " " + data['header']['instance'] + " " +
                                     data['header']['modulo'] + " " + data['header']['date'] + " " +
                                     data['header']['filename'] + " " + self.tech + " " + line)
                if linearray:
                    for line2 in linearray:
                        f.write(line2+"\n")
        else:
            # TODO: METEMOS LAS NUEVAS LINEAS POR EL FINAL DEL FICHERO Y ELIMINAMOS DEL PRINCIPIO
            pass

    def _sendBufferAgent(self):
        ##EL BUFFER SE DEBE VACIAR EL TERMINAR EL WRITE
        self._sendCacheAgent()
        for hash, data in self._buffer.iteritems():
            ##ENVIAMOS LOS DATOS AL AGENTE COLLECTOR
            ret = self._send(data)
            if 'lines' in ret and (ret['lines'] == len(data['body']) or ret['lines'] == -1):
                LOG.info("Metricas enviadas correctamente al agente. Series: %s", str(ret['lines']),
                         extra={'monitor': data['header']['technology'], 'modulo': data['header']['modulo']})
            else:
                # HA HABIDO ALGUN ERROR
                # GUARDAMOS EN CACHE LO QUE NO SE HA PODIDO ENVIAR
                LOG.info("Metricas no enviadas. Guardadas en cache %s series.", str(len(data['body'])),
                         extra={'monitor': data['header']['technology'], 'modulo': data['header']['modulo']})
                self._addToCache(data)

        self._buffer = {}
