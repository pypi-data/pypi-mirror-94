# coding=utf-8
import copy

import m360
import m360.base.instance as base
from m360.agents.internal.settings import  Settings
import sys
class Instance (base.Instance):

    ALLOWED_MODULES = [ Settings.INTERNAL_MEMSTATS, Settings.INTERNAL_AGENT, Settings.INTERNAL_GATHER, Settings.INTERNAL_WRITE ]

    def __init__(self,name,host,conf,queue):
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self._version = m360.__version__
        self._data = copy.deepcopy(conf['_data'] if "_data" in conf else Settings.INTERNAL)
        self.queue = queue
        if "service" not in self.global_tags:
            self.global_tags['service'] = "Telegraf"
        if "os" not in self.global_tags:
            self.global_tags['os'] = sys.platform.replace("Linux","Unix")
        if "group" not in self.global_tags:
            self.global_tags['group'] = "MONITOR"

    def read_queue(self):
        ##INTERNAL METRICS
        if self.queue:
            while not self.queue.empty():
                stats = self.queue.get()
                # MERGE STATS
                for measurement,metrics in stats.items():
                    if measurement not in self._data:
                        self._data[measurement] = copy.deepcopy(metrics)
                    else:
                        for var,val in metrics.items():
                            if var=="global":
                                continue
                            if isinstance(val,dict):
                                if var not in self._data[measurement]:
                                    self._data[measurement][var]=copy.deepcopy(val)
                                else:
                                    for var2, val2 in val.items():
                                        if isinstance(val2,str):
                                            self._data[measurement][var][var2]=val2
                                        else:
                                            self._data[measurement][var][var2]=self._data[measurement][var][var2]+val2
                            elif isinstance(val, str):
                                self._data[measurement][var]=val
                            else:
                                self._data[measurement][var]=self._data[measurement][var]+val
        return self._data

    def agent(self):
        data=self.read_queue()
        return [data["internal_agent"]]

    def write(self):
        retdata=[]
        data=self.read_queue()
        for output,metrics in data["internal_write"].items():
            if output!="global":
                newm = copy.deepcopy(metrics)
                newm['output']=output
                retdata.append(newm)
        return retdata

    def memstats(self):
        data=self.read_queue()
        return [data["internal_memstats"]]

    def gather(self):
        retdata=[]
        data=self.read_queue()
        for input,metrics in data["internal_gather"].items():
            if input!="global":
                newm = copy.deepcopy(metrics)
                newm['input']=input
                retdata.append(newm)
        return retdata
