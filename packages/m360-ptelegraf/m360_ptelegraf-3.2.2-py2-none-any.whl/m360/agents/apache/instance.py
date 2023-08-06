# coding=utf-8
import m360.base.instance as base
from m360.agents.apache.settings import  Settings
from m360.agents.apache.manager import Manager


class Instance (base.Instance):

    ALLOWED_MODULES = [ Settings.HTTP, Settings.THREADS , Settings.ACCESS]

    def __init__(self,name,host,conf):
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self._server_status = None
        self._version = None

    def threads(self):
        arrmetrics=[]
        data = self._loadserverstatus()
        if data and 'scoreboard' in data:
            arrmetrics.append(data['scoreboard'])
        return arrmetrics

    def access(self):
        data = Manager.getaccessmetrics(self)
        return data

    def http(self):
        arrmetrics=[]
        data = self._loadserverstatus()
        if data and 'status' in data:
            arrmetrics.append(data['status'])
        return arrmetrics

    def _loadserverstatus(self):
        if not self._server_status:
            self._server_status = Manager.status(self.conf['endpoint'])

        if not self._version:
            if "ServerVersion" in self._server_status:
                self._version = self._server_status['ServerVersion']

        return self._server_status

    def isrunning(self):
        if Settings.DEBUG:
            return True

        ret = False
        try:
            laststatus=self._loadserverstatus()
            if 'code' in laststatus:
                return True
        except Exception as e:
            ret = False
        return ret
