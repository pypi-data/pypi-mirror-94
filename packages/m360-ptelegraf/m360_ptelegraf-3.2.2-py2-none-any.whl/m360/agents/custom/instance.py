# coding=utf-8
import os
import sys
from importlib import import_module

from m360.agents.custom.settings import Settings
import m360.base.instance as base


class Instance (base.Instance):

    ALLOWED_MODULES = [Settings.MODULE]

    def __init__(self,name,host,conf):
        ##CONFIGURAR LA TECH
        _tech = "demo"
        conf['Technology'] = "demo"
        ##CONFIGURAR LOS MODULOS
        _allowed  = []
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,_allowed,name,host,conf)
        self._version=None

    #EL HOST DE LA INSTANCIA SE RECUPERA DEL ADMINSERVER Y ES LA MACHINE DONDE ESTA
    def isrunning(self):
        return True

    def health(self):
        return 1

    def __getattr__(self, item):
        if item in self.modules:
            m_path = os.path.dirname(self.conf['script'])
            ##TODO: ESTO PUEDE HACER COSAS RARAS
            sys.path.append(m_path)
            m_name = os.path.basename(self.conf['script']).replace(".py", "")
#            p, m = self.conf['script'].rsplit('.', 1)
            moduleObj = __import__(m_name, fromlist=[item])
#            moduleObj = import_module(m_name)
            if not hasattr(moduleObj,item):
                raise NotImplementedError("Not defined "+item+"() in "+self.conf['script'])
            algo = getattr(moduleObj,item)
            return algo
        else:
            return getattr(super(Instance,self),item)
