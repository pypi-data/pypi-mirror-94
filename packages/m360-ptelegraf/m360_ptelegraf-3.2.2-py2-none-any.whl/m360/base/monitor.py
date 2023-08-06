# coding=utf-8
import copy
import ctypes
import random
import threading
import urllib2
from m360.base.telegraf_compat import get_tag_compat,get_field_compat,get_measurement_compat
from m360.base.lib.loadbalancer import LoadBalancer
import os
import m360.base.settings as base
import m360.base.errores as returncodes
import csv
import datetime
import time
from logging import getLogger
from importlib import import_module

LOG = getLogger('m360.base')

try:
    import ssl
except ImportError as e:
    LOG.error("SSL no instalado. {}", e.message, extra={'monitor': "NA", 'modulo': "NA"})


def process_wrapper(fname, chunkStart, chunkSize, processObj, funcPars):
    with open(fname, 'r') as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        reader = csv.reader(lines, delimiter=' ')
    for line in reader:
        funcPars['stats'] = processObj.processLine(line,funcPars)
    return funcPars['stats']


class Monitor(threading.Thread):

    def __init__(self, tech, instances, outputs, service, host,queue=None,loop=False):
        super(Monitor, self).__init__(name=tech+"-"+str(random.randint(0,99999)))
        self.loop=loop
        self.delay=0
        self._service = service
        self.tech=tech
        self.host=host
        self.instances=instances
        self._outputs = outputs
        self.queue = queue
        self.stats = copy.deepcopy(base.Settings.INTERNAL)
        for odict in outputs:
            for o,confi in odict.items():
                self.stats['internal_write'][o]=copy.deepcopy(base.Settings.INTERNAL['internal_write']['global'])
        if instances:
            for i in instances[0].modules:
                self.stats['internal_gather'][get_measurement_compat(self.tech,i)] = copy.deepcopy(base.Settings.INTERNAL['internal_gather']['global'])

    def chunkify(self,fname, startpos, endpos, size=base.Settings.FILE_BUFFER_READ):
        fileEnd = endpos
        chunkEnd = startpos
        with open(fname, 'r') as f:
            while True:
                chunkStart = chunkEnd
                f.seek(size, 1)
                f.readline()
                chunkEnd = f.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break

    def _write(self,host,instance,modulo,metricasobj):
        ###POR CADA OUTPUT CONFIGURADO
        outputs = instance.outputs if instance.outputs else self._outputs
        for i in outputs:
            for output,conf in i.items():
                module = import_module("m360.outputs."+output)
                outputObj=module.Output(instance,conf)
                timexecute=time.time()
                outputObj.write(host,modulo,metricasobj)
                timexecute=time.time()-timexecute
                self.stats['internal_write'][output]['metrics_written']=self.stats['internal_write'][output]['metrics_written']+len(metricasobj)
                self.stats['internal_write'][output]['write_time_ns']=self.stats['internal_write'][output]['write_time_ns']+int(timexecute*1000*1000*1000)
                self.stats['internal_agent']['metrics_written'] = self.stats['internal_agent']['metrics_written'] + len(metricasobj)
                LOG.debug("Output '%s' en %.3f segs.",output,timexecute, extra={'monitor': instance.tech, 'modulo': modulo})

    def run(self):
        while True:
            if self.delay>0:
                time.sleep(self.delay)
            for instance in self.instances:
                if instance.isrunning():
                    for modulo in instance.modules:
                        try:
                            LOG.debug("Extrayendo metricas de %s.",instance.name,extra={'monitor':instance.tech,'modulo':modulo})
                            timexecute = time.time()
                            metricasobj=getattr(instance,modulo)()
                            timexecute = time.time() - timexecute
                            self._write(self.host,instance,modulo,metricasobj)
                            self.stats['internal_agent']['metrics_gathered'] = self.stats['internal_agent']['metrics_gathered'] + len(metricasobj)
                            self.stats['internal_gather'][get_measurement_compat(self.tech,modulo)]['metrics_gathered'] = self.stats['internal_gather'][get_measurement_compat(self.tech,modulo)]['metrics_gathered'] + len(metricasobj)
                            self.stats['internal_gather'][get_measurement_compat(self.tech,modulo)]['gather_time_ns'] = self.stats['internal_gather'][get_measurement_compat(self.tech,modulo)]['gather_time_ns'] + int(timexecute * 1000 * 1000 * 1000)
                            LOG.debug("Metricas extraidas de %s.",instance.name,extra={'monitor':instance.tech,'modulo':modulo})
                        except NotImplementedError as e:
                            self.stats['internal_agent']['gather_errors'] = self.stats['internal_agent']['gather_errors'] + 1
                            LOG.warning("Modulo no definido.",extra={'monitor':instance.tech,'modulo':modulo})
                        except Exception as e:
                            self.stats['internal_agent']['gather_errors'] = self.stats['internal_agent']['gather_errors'] + 1
                            LOG.warning("Error inesperado en el modulo. (%s).",str(e),extra={'monitor':instance.tech,'modulo':modulo})
                            if base.Settings.DEBUG:
                                raise e
#                if instance.tech not in ["ovo","internal"]:
#                    LOG.debug("Extrayendo metricas de %s.", instance.name,
#                                  extra={'monitor': instance.tech, 'modulo': 'health'})
#                    health_response = instance.healthcheck()
#                    if type(health_response) is dict:
#                        self._write(self.host, instance, "health", [health_response])
#                    else:
#                        self._write(self.host, instance, "health", [{'status_code': health_response}])
#                    LOG.debug("Extrayendo metricas de %s.", instance.name, extra={'monitor': instance.tech, 'modulo': 'health'})
            if self.queue:
                self.queue.put(self.stats)
            if not self.loop:
                break

        return returncodes.OK

    def stop(self):
        self.loop = False

    def raise_exception(self):
        thread_id = self.ident
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')