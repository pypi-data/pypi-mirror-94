from m360.base.settings import Settings
import os
import random
from logging import getLogger
import socket
import time

LOG = getLogger('m360.base.lib')

class LoadBalancer(object):

    def __init__(self,pool,monitor,randomize=True,jumpifzero=True,persistence=True,expire=300,timeout=1.0):
        self._timeout=timeout
        self._pool=pool
        self._randomize=randomize
        self._jumpifzero=jumpifzero
        self._persistence=persistence
        self._last=None
        self._expire=expire
        self._filename=os.path.join(Settings.MONITOR_CACHE,"__agent_collector_node."+monitor)
        delta=0
        try:
            delta=time.time()-os.stat(self._filename).st_mtime
        except Exception as e:
            pass
        if persistence and delta<expire:
            try:
                with open(self._filename,"r") as f:
                    self._last=f.read()
            except Exception as e:
                LOG.warning("Not read lbnode file '%s' Exception is %s",self._filename,
                                            str(e),extra={"monitor": "na", "modulo": "na"})

    def ping(self,ip,port):
        #HACEMOS TELNET AL IP:PUERTO
        s = socket.socket()
        address = ip
        ret=False
        try:
            s.settimeout(self._timeout)
            s.connect((address, port))
            s.settimeout(None)
            # originally, it was
            # except Exception, e:
            # but this syntax is not supported anymore.
            ret=True
        except Exception as e:
            LOG.debug("Not ping via socket with %s:%d. Exception is %s", address, port,str(e),
                                      extra={"monitor": "na", "modulo": "na"})
        finally:
            s.close()
        return ret

    def removefrompool(self,ip):
        #DESCARTAMOS ESTE NODO DEL POOL
        newpool=[]
        for cpd in self._pool:
            newcpd=[]
            for nodo in cpd:
                if nodo!=ip:
                    newcpd.append(nodo)
            newpool.append(newcpd)
        return newpool

    def getip(self,port):
        if self._last and self.ping(self._last,port):
            return self._last

        if self._last:
            self._pool=self.removefrompool(self._last)

        clusters=[]
        if len(self._pool)>0:
            if type(self._pool[0]) in (dict,list):
                if not self._jumpifzero:
                    clusters=self._pool[0]
                else:
                    clusters=self._pool
            else:
                clusters=[self._pool]

        for cpd in clusters:
            rango=range(len(cpd))
            if self._randomize:
                rango=random.sample(rango,len(rango))
            for i in rango:
                if self.ping(cpd[i],port):
                    try:
                        with open(self._filename,"w") as f:
                            f.write(cpd[i])
                        self._last=cpd[i]
                    except Exception as e:
                        LOG.error("Not write lbnode file '%s' Exception is %s",self._filename,
                                                  str(e),extra={"monitor": "na", "modulo": "na"})

                    return cpd[i]
                else:
                    self._pool=self.removefrompool(cpd[i])

        return None
