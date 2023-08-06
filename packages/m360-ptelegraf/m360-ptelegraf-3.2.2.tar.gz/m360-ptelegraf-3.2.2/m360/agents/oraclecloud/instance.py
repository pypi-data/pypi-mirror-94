# coding=utf-8
import m360.base.instance as base
from m360.agents.oraclecloud.settings import  Settings
from m360.agents.oraclecloud.manager import Manager
from logging import getLogger

LOG = getLogger('m360.agents.oraclecloud')


class Instance(base.Instance):

    ALLOWED_MODULES = [Settings.AUTONOMOUS]

    def __init__(self,name,host,conf):
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self._manager = Manager(conf['ocifile'])
        self.global_tags('host',None)

    def oci_autonomous_database(self):
        data = None
        try:
            data = self._manager.get_autonomous(self._conf['compartment_id'])
        except Exception as e:
            LOG.error("Error %s", str(e),extra={"monitor":self.tech,"modulo":"autonomous"})

        return data

    def isrunning(self):
        return 1
