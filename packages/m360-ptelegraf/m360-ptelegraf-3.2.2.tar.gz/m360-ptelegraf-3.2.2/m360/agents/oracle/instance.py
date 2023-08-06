# coding=utf-8
import time

import m360.base.instance as base
from m360.agents.oracle.settings import  Settings
from m360.agents.oracle.manager import Manager
from logging import getLogger
import copy

LOG=getLogger('m360.agents.oracle')

class Instance (base.Instance):

    ALLOWED_MODULES = Settings.ORACLE_MODULES

    def __init__(self,name,host,conf):
        super(Instance,self).__init__(Settings.MONITOR_TECHNOLOGY,Instance.ALLOWED_MODULES,name,host,conf)
        self.data=None
        self._jvmversion=None
        self._jvmversion = conf['jvmversion'] if 'jvmversion' in conf else ""
        self._manager = Manager(persistent=True,**conf)
        self._version=conf['version'] if 'version' in conf else self._manager.execute('version2')

    def isrunning(self):
        try:
            ret = self._manager.execute('check_active',instance=self.name)
        except Exception as e:
            LOG.error("Error %s", str(e),extra={"monitor":self.tech,"modulo":"isrunning"})
            ret = False
        return ret

    def health(self):
        __ORACLE_STATES={"UNKOWN":-1,"SHUTDOWN":0,"OPEN":1,"STARTED":2,"MOUNTED":3,"OPEN MIGRATE":4,"STANDBY":5,"SUSPENDED":6,"FORCE_SUSPENDING":7,"SHUTTING_DOWN":8}
        status=self._manager.execute('status',instance=self.name,force=True)
        if 'database_status' in status:
            if status['database_status']=='ACTIVE':
                status_code=__ORACLE_STATES[status['status']] if status['status'] in __ORACLE_STATES else -1
            else:
                status_code=__ORACLE_STATES[status['database_status']] if status['database_status'] in __ORACLE_STATES else -1
            status['status_code'] = status_code
        else:
            status={'database_status':'UNKWOWN','status':'UNKOWN','status_code':-1}

        return status

    def users(self):
        ret = []
        __USER_STATUS = {
            'OPEN':0,
            'EXPIRED':1,
            'EXPIRED(GRACE)':2,
            'LOCKED(TIMED)':3,
            'LOCKED':4,
            'EXPIRED & LOCKED(TIMED)':5,
            'EXPIRED(GRACE) & LOCKED(TIMED)':6,
            'EXPIRED & LOCKED':7,
            'EXPIRED(GRACE) & LOCKED':8
        }

        users = self._manager.execute('users_status')
        for u in users:
            newval = {}
            newval['status_code']=__USER_STATUS[u['STATUS']] if u['STATUS'] in __USER_STATUS else -1
            newval['user'] = u['DBUSER']
            newval['status'] = u['STATUS']
            if u['LDATE']:
                newval['locked'] = int(time.mktime(u['LDATE'].timetuple()))
            if u['EDATE']:
                newval['expire'] = int(time.mktime(u['EDATE'].timetuple()))
            ret.append(newval)
        return ret

    def asm(self):
        ret = []
        asm = self._manager.execute('show_asm_volumes')
        for a in asm:
            val = self._manager.execute('asm_volume_use',name=a['ASMVOLUME'])
            if val:
                ret.append({'total':val['TOTAL'],'free':val['FREE'],'used':val['USED'],'used_prc':val['PRC']})
        return ret

    def storage(self):
        ret = {}
        stats = ['dbsize','dbfilesize']
        for s in stats:
            val = self._manager.execute(s)
            if val is not None:
                ret[s] = val
        return [ret]

    def tablespaces(self):
        ret = []
        tablespaces = self._manager.execute('show_tablespaces')
        for t in tablespaces:
            newval={}
            val = self._manager.execute('tablespace_abs',name=t['TABLESPACE'])
            if val:
                newval['total']= val['TOTAL']
                newval['free'] = val['FREE']
                newval['used'] = val['USED']
                newval['used_prc'] = round(100.0*float(val['USED'])/float(val['TOTAL']),2)
            else:
                continue
            val = self._manager.execute('tablespace',name=t['TABLESPACE'])
            if val:
                newval['usage']=float(val)
            if newval:
                newval['name'] = t['TABLESPACE']
                ret.append(newval)

        tablespaces = self._manager.execute('show_tablespaces_temp')
        for t in tablespaces:
            val = self._manager.execute('tablespace_temp',name=t['TABLESPACE_TEMP'])
            if val:
                ret.append({"name":t['TABLESPACE_TEMP'],"free":val['FREE'],"total":val['TOTAL'],"used":val['USED'],"used_prc":float(val['PRC'])})
        return ret

    def log(self):
        ret = {}
        stats = ['lastapplarclog','lastarclog','query_redologs']
        for s in stats:
            val = self._manager.execute(s)
            if val is not None:
                ret[s] = val
        return [ret]

    def events(self):
        ret = {}
        stats = [
            'freebufwaits',
            'bufbusywaits',
            'logswcompletion',
            'logfilesync',
            'logprllwrite',
            'enqueue',
            'dbseqread',
            'dbscattread',
            'dbsnglwrite',
            'dbprllwrite',
            'directread',
            'directwrite',
            'latchfree'
        ]
        for s in stats:
            val = self._manager.execute(s)
            if val is not None:
                ret[s] = val
        return [ret]

    def sysstat(self):
        ret = {}
        stats = [
            'rcachehit',
            'dsksortratio',
            'commits',
            'rollbacks',
            'deadlocks',
            'redowrites',
            'tblscans',
            'tblrowsscans',
            'indexffs',
            'hparsratio',
            'netsent',
            'netresv',
            'netroundtrips',
            'logonscurrent'
        ]
        for s in stats:
            val = self._manager.execute(s)
            if val is not None:
                ret[s] = val
            else:
                LOG.debug("Cannot get metric %s", s, extra={"monitor": self.tech, "modulo": "sysstat"})
        return [ret]

    def database(self):
        ret = {}
        stats = ['uptime','query_lock','fra_use','activeusercount']
        extra_metrics = []
        if 'extra_metrics' in self.conf:
            extra_metrics = self.conf['extra_metrics']
        for s in stats:
            val = self._manager.execute(s)
            if val is not None:
                ret[s] = val
        if extra_metrics:
            metrics = self._manager.execute('query_sysmetrics',name=extra_metrics)
            for m in metrics:
                ret[m['METRIC'].lower().replace(" ","_")] = m['VALUE']
        return [ret]

    def sessions(self):
        ret = {}
        stats = ['query_sessions','query_rollbacks']
        for s in stats:
            val = self._manager.execute(s)
            if val is not None:
                ret[s] = val
        return [ret]
