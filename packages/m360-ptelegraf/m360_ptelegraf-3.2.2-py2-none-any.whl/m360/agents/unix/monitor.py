import m360.base.monitor as base
from m360.agents.unix.instance import Instance
from m360.agents.unix.settings import Settings


class Monitor (base.Monitor):
    def __init__(self,host,user=None, settings=None,outputs=None,service=None,queue=None):
        instances = []
        m_outputs = []
        if settings is None:
            settings = []
        if outputs is None:
            outputs = []
        self._conf={}
        for name, conf in settings.items():
            if name.startswith("outputs."):
                m_outputs.append({name.split(".")[1]:conf})
            elif isinstance(conf,dict):
                instance_name = name
                if "instance" in conf:
                    instance_name = conf['instance']
                instances.append(Instance(instance_name, host, conf))
            else:
                self._conf[name] = conf
        super(Monitor,self).__init__(Settings.MONITOR_TECHNOLOGY,
                                     instances,
                                     m_outputs if m_outputs else outputs,
                                     service,
                                     host,queue=queue)


