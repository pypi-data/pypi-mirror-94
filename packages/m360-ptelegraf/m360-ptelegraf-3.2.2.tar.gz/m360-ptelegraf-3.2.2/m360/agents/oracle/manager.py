import cx_Oracle
import json
from logging import getLogger

LOG=getLogger('m360.agents.oracle')

version = 0.2
###CREATE USER M360 IDENTIFIED BY  DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE TEMP PROFILE DEFAULT ACCOUNT UNLOCK;
###GRANT CONNECT TO M360;
###GRANT RESOURCE TO M360;
###ALTER USER M360 DEFAULT ROLE ALL;
###GRANT SELECT ANY TABLE TO M360;
###GRANT CREATE SESSION TO M360;
###GRANT SELECT ANY DICTIONARY TO M360;
###GRANT UNLIMITED TABLESPACE TO M360;
###GRANT SELECT ANY DICTIONARY TO M360;
###GRANT SELECT ON V_$SESSION TO M360;
###GRANT SELECT ON V_$SYSTEM_EVENT TO M360;
###GRANT SELECT ON V_$EVENT_NAME TO M360;
###GRANT SELECT ON V_$RECOVERY_FILE_DEST TO M360;

class Manager(object):
    def check_active(self,instance):
        """Check Intance is active and open"""
        sql = "select to_char(case when inst_cnt > 0 then 1 else 0 end, \
              'FM99999999999999990') retvalue from (select count(*) inst_cnt \
              from v$instance where status = 'OPEN' and logins = 'ALLOWED' \
              and database_status = 'ACTIVE' and instance_name = '{0}')".format(instance)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        ret = False
        for i in res:
            ret = i[0] == '1'
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "check_active"})
        return ret

    def status(self,instance):
        """Check Intance is active and open"""
        sql = "select status,database_status from v$instance where instance_name = '{0}'".format(instance)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        ret = {}
        for i in res:
            ret={'status':i[0].upper(),'database_status':i[1].upper()}
            LOG.debug("Sql: %s,Result: %s",sql, str(i), extra={"monitor": 'oracle', "modulo": "status"})
        return ret

    def rcachehit(self):
        """Read Cache hit ratio"""
        sql = "SELECT nvl(to_char((1 - (phy.value - lob.value - dir.value) / \
              ses.value) * 100, 'FM99999990.9999'), '0') retvalue \
              FROM   v$sysstat ses, v$sysstat lob, \
              v$sysstat dir, v$sysstat phy \
              WHERE  ses.name = 'session logical reads' \
              AND    dir.name = 'physical reads direct' \
              AND    lob.name = 'physical reads direct (lob)' \
              AND    phy.name = 'physical reads'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "rcachehit"})
            return i[0]
        return None

    def dsksortratio(self):
        """Disk sorts ratio"""
        sql = "SELECT nvl(to_char(d.value/(d.value + m.value)*100, \
              'FM99999990.9999'), '2') retvalue \
              FROM  v$sysstat m, v$sysstat d \
              WHERE m.name = 'sorts (memory)' \
              AND d.name = 'sorts (disk)'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "dsksortratio"})
            return i[0]
        return None

    def activeusercount(self):
        """Count of active users"""
        sql = "select to_char(count(*)-1, 'FM99999999999999990') retvalue \
              from v$session where username is not null \
              and status='ACTIVE'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "activeusercount"})
            return i[0]
        return None

    def dbsize(self):
        """Size of user data (without temp)"""
        sql = "SELECT to_char(sum(  NVL(a.bytes - NVL(f.bytes, 0), 0)), \
              'FM99999999999999990') retvalue \
              FROM sys.dba_tablespaces d, \
              (select tablespace_name, sum(bytes) bytes from dba_data_files \
              group by tablespace_name) a, \
              (select tablespace_name, sum(bytes) bytes from \
              dba_free_space group by tablespace_name) f \
              WHERE d.tablespace_name = a.tablespace_name(+) AND \
              d.tablespace_name = f.tablespace_name(+) \
              AND NOT (d.extent_management like 'LOCAL' AND d.contents \
              like 'TEMPORARY')"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "dbsize"})
            return i[0]
        return None

    def dbfilesize(self):
        """Size of all datafiles"""
        sql = "select to_char(sum(bytes), 'FM99999999999999990') retvalue \
              from dba_data_files"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s", sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "dbfilesize"})
            return i[0]
        return None

    def version(self):
        """Oracle version (Banner)"""
        sql = "select banner from v$version where rownum=1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "version"})
            return i[0]
        return None

    def uptime(self):
        """Instance Uptime (seconds)"""
        sql = "select to_char((sysdate-startup_time)*86400, \
              'FM99999999999999990') retvalue from v$instance"
        self.cur.execute(sql)
        res = self.cur.fetchmany(numRows=3)
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "uptime"})
            return i[0]
        return None

    def commits(self):
        """User Commits"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'user commits'"
        self.cur.execute(sql)
        res = self.cur.fetchmany(numRows=3)
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "commits"})
            return i[0]
        return None

    def rollbacks(self):
        """User Rollbacks"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from " \
              "v$sysstat where name = 'user rollbacks'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s", sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "rollbacks"})
            return i[0]
        return None

    def deadlocks(self):
        """Deadlocks"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'enqueue deadlocks'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "deadlocks"})
            return i[0]
        return None

    def redowrites(self):
        """Redo Writes"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'redo writes'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "redowrites"})
            return i[0]
        return None

    def tblscans(self):
        """Table scans (long tables)"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'table scans (long tables)'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s", sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "tblscans"})
            return i[0]
        return None

    def tblrowsscans(self):
        """Table scan rows gotten"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'table scan rows gotten'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "tblrowsscans"})
            return i[0]
        return None

    def indexffs(self):
        """Index fast full scans (full)"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'index fast full scans (full)'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "indexffs"})
            return i[0]
        return None

    def hparsratio(self):
        """Hard parse ratio"""
        sql = "SELECT nvl(to_char(h.value/t.value*100,'FM99999990.9999'), '0') \
              retvalue FROM  v$sysstat h, v$sysstat t WHERE h.name = 'parse count (hard)' AND t.name = 'parse count (total)'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "hparsratio"})
            return i[0]
        return None

    def netsent(self):
        """Bytes sent via SQL*Net to client"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'bytes sent via SQL*Net to client'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s", sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "netsent"})
            return i[0]
        return None

    def netresv(self):
        """Bytes received via SQL*Net from client"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'bytes received via SQL*Net from client'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "netresv"})
            return i[0]
        return None

    def netroundtrips(self):
        """SQL*Net roundtrips to/from client"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'SQL*Net roundtrips to/from client'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "netroundtrips"})
            return i[0]
        return None

    def logonscurrent(self):
        """Logons current"""
        sql = "select nvl(to_char(value, 'FM99999999999999990'), '0') retvalue from \
              v$sysstat where name = 'logons current'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "logonscurrent"})
            return i[0]
        return None

    # TODO: DEvuelve NONE
    def lastarclog(self):
        """Last archived log sequence"""
        sql = "select to_char(max(SEQUENCE#), 'FM99999999999999990') \
              retvalue from v$log where archived = 'YES'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s", sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "lastarclog"})
            return i[0]
        return None

    #TODO: DEvuelve NONE
    def lastapplarclog(self):
        """Last applied archive log (at standby).Next items requires
        [timed_statistics = true]
        In Oracle 9i and beyond, the DBMS_SYSTEM.SET_INT_PARAM_IN_SESSION package
        can be used to alter the settings of session alterable parameters."""
        sql = "ALTER SESSION SET TIMED_STATISTICS=TRUE"
        self.cur.execute(sql)
        sql = "select to_char(max(lh.SEQUENCE#), 'FM99999999999999990') \
              retvalue from v$loghist lh, v$archived_log al \
              where lh.SEQUENCE# = al.SEQUENCE# and applied='YES'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "lastapplarclog"})
            return i[0]
        return None

    def freebufwaits(self):
        """Free buffer waits"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en \
              where se.event(+) = en.name and en.name = 'free buffer waits'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "freebufwaits"})
            return i[0]
        return None

    def bufbusywaits(self):
        """Buffer busy waits"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) = \
              en.name and en.name = 'buffer busy waits'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "bufbusywaits"})
            return i[0]
        return None

    def logswcompletion(self):
        """log file switch completion"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'log file switch completion'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "logswcompletion"})
            return i[0]
        return None

    def logfilesync(self):
        """Log file sync"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en \
              where se.event(+) = en.name and en.name = 'log file sync'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s", sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "logfilesync"})
            return i[0]
        return None

    def logprllwrite(self):
        """Log file parallel write"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'log file parallel write'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "logprllwrite"})
            return i[0]
        return None

    def enqueue(self):
        """Enqueue waits"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en \
              where se.event(+) = en.name and en.name = 'enqueue'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "enqueue"})
            return i[0]
        return 0

    def dbseqread(self):
        """DB file sequential read waits"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'db file sequential read'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "dbseqread"})
            return i[0]
        return None

    def dbscattread(self):
        """DB file scattered read"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'db file scattered read'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "dbscattread"})
            return i[0]
        return None

    def dbsnglwrite(self):
        """DB file single write"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'db file single write'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "dbsnglwrite"})
            return i[0]
        return None

    def dbprllwrite(self):
        """DB file parallel write"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'db file parallel write'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "dbprllwrite"})
            return i[0]
        return None

    def directread(self):
        """Direct path read"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'direct path read'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "directread"})
            return i[0]
        return None

    def directwrite(self):
        """Direct path write"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'direct path write'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s", sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "directwrite"})
            return i[0]
        return None

    def latchfree(self):
        """latch free"""
        sql = "select nvl(to_char(time_waited, 'FM99999999999999990'), '0') retvalue \
              from v$system_event se, v$event_name en where se.event(+) \
              = en.name and en.name = 'latch free'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "latchfree"})
            return i[0]
        return None

    def tablespace(self, name):
        """Get tablespace usage"""
        sql = '''SELECT  tablespace_name,
        100-(TRUNC((max_free_mb/max_size_mb) * 100)) AS USED
        FROM ( SELECT a.tablespace_name,b.size_mb,a.free_mb,b.max_size_mb,a.free_mb + (b.max_size_mb - b.size_mb) AS max_free_mb
        FROM   (SELECT tablespace_name,TRUNC(SUM(bytes)/1024/1024) AS free_mb FROM dba_free_space GROUP BY tablespace_name) a,
        (SELECT tablespace_name,TRUNC(SUM(bytes)/1024/1024) AS size_mb,TRUNC(SUM(GREATEST(bytes,maxbytes))/1024/1024) AS max_size_mb
        FROM   dba_data_files GROUP BY tablespace_name) b WHERE  a.tablespace_name = b.tablespace_name
        ) where tablespace_name='{0}' order by 1'''.format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i), extra={"monitor": 'oracle', "modulo": "tablespace"})
            return i[1]
        return None

    def tablespace_abs(self, name):
        """Get tablespace in use"""
        sql = '''SELECT df.tablespace_name "TABLESPACE", (df.totalspace - \
              tu.totalusedspace) "FREE",df.totalspace "TOTAL",tu.totalusedspace "USED" from (select tablespace_name, \
              sum(bytes) TotalSpace from dba_data_files group by tablespace_name) \
              df ,(select sum(bytes) totalusedspace,tablespace_name from dba_segments \
              group by tablespace_name) tu WHERE tu.tablespace_name = \
              df.tablespace_name and df.tablespace_name = '{0}' '''.format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i), extra={"monitor": 'oracle', "modulo": "tablespace_abs"})
            return {"TOTAL":i[2],"FREE":i[1],"USED":i[3]}
        return None

    def show_tablespaces(self):
        """List tablespace names in a JSON like format for Zabbix use"""
        sql = "SELECT tablespace_name FROM dba_tablespaces ORDER BY 1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['TABLESPACE']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        LOG.debug("Sql: %s,Result: %s", sql, json.dumps({'data': lst}), extra={"monitor": 'oracle', "modulo": "show_tablespaces"})
        return lst

    def show_tablespaces_temp(self):
        """List temporary tablespace names in a JSON like
        format for Zabbix use"""
        sql = "SELECT TABLESPACE_NAME FROM DBA_TABLESPACES WHERE \
              CONTENTS='TEMPORARY'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['TABLESPACE_TEMP']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        LOG.debug("Sql: %s,Result: %s",sql, json.dumps({'data': lst}), extra={"monitor": 'oracle', "modulo": "show_tablespaces_temp"})
        return lst

    def check_archive(self, archive):
        """List archive used"""
        sql = "select trunc((total_mb-free_mb)*100/(total_mb)) PCT,free_mb FREE,total_mb-free_mb USED,total_mb TOTAL from \
              v$asm_diskgroup_stat where name='{0}' \
              ORDER BY 1".format(archive)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i), extra={"monitor": 'oracle', "modulo": "check_archive"})
            return {"PCT":i[0],"FREE":i[1],"USED":i[2],"TOTAL":i[3]}
        return None

    def show_asm_volumes(self):
        """List als ASM volumes in a JSON like format for Zabbix use"""
        sql = "select NAME from v$asm_diskgroup_stat ORDER BY 1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['ASMVOLUME']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        LOG.debug("Query: %s, Result: %s", sql,json.dumps({'data': lst}), extra={"monitor": 'oracle', "modulo": "show_asm_volumes"})
        return lst

    def asm_volume_use(self, name):
        """Get ASM volume usage"""
        sql = "select round(((TOTAL_MB-FREE_MB)/TOTAL_MB*100),2),FREE_MB FREE,TOTAL_MB-FREE_MB USED,TOTAL_MB TOTAL  from \
              v$asm_diskgroup_stat where name = '{0}'".format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "asm_volume_use"})
            return {"PCT":i[0],"FREE":i[1],"USED":i[2],"TOTAL":i[3]}
        return None

    def query_lock(self):
        """Query lock"""
        sql = "SELECT count(*) FROM gv$lock l WHERE  block=1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s", sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "query_lock"})
            return i[0]
        return None

    def query_redologs(self):
        """Redo logs"""
        sql = "select COUNT(*) from v$LOG WHERE STATUS='ACTIVE'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "query_redologs"})
            return i[0]
        return None

    def query_rollbacks(self):
        """Query Rollback"""
        sql = "select nvl(trunc(sum(used_ublk*4096)/1024/1024),0) from \
              gv$transaction t,gv$session s where ses_addr = saddr"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "query_rollbacks"})
            return i[0]
        return None

    def query_sessions(self):
        """Query Sessions"""
        sql = "select count(*) from gv$session where username is not null \
              and status='ACTIVE'"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "query_sessions"})
            return i[0]
        return None

    def tablespace_temp(self, name):
        """Query temporary tablespaces"""
        sql = "SELECT round(((TABLESPACE_SIZE-FREE_SPACE)/TABLESPACE_SIZE)*100,2) \
              PERCENTUAL,TABLESPACE_SIZE,FREE_SPACE,TABLESPACE_SIZE-FREE_SPACE \"USED\" FROM dba_temp_free_space where \
              tablespace_name='{0}'".format(name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "tablespace_temp"})
            return {"PRC":i[0],"FREE":i[2],"TOTAL":i[1],"USED":i[3] }
        return None

    def query_sysmetrics(self, name):
        """Query v$sysmetric parameters"""
        if "*" in name:
            sql = "select METRIC_NAME,value from v$sysmetric order by INTSIZE_CSEC"
        else:
            sql = "select METRIC_NAME,value from v$sysmetric where METRIC_NAME IN ('{0}') order by INTSIZE_CSEC".format("','".join(name))
        self.cur.execute(sql)
        res = self.cur.fetchall()
        lst=[]
        key = ['METRIC','VALUE']
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        LOG.debug("Sql: %s,Result: %s", sql, str(lst), extra={"monitor": 'oracle', "modulo": "query_sysmetrics"})
        return lst

    def show_sysmetrics(self):
        """Query v$sysmetric parameters"""
        sql = "select METRIC_NAME,value from v$sysmetric order by INTSIZE_CSEC"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        lst=[]
        key = ['METRIC']
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "show_sysmetrics"})
        return lst

    def fra_use(self):
        """Query the Fast Recovery Area usage"""
        sql = "select round((SPACE_LIMIT-(SPACE_LIMIT-SPACE_USED))/ \
              SPACE_LIMIT*100,2) FROM V$RECOVERY_FILE_DEST"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "fra_use"})
            return i[0]
        return None

    def show_users(self):
        """Query the list of users on the instance"""
        sql = "SELECT username FROM dba_users ORDER BY 1"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        key = ['DBUSER']
        lst = []
        for i in res:
            d = dict(zip(key, i))
            lst.append(d)
        LOG.debug("Sql: %s,Result: %s",sql, json.dumps({'data': lst}), extra={"monitor": 'oracle', "modulo": "show_users"})
        return lst

    def users_status(self):
        """Determines whether a user is locked or not"""
        sql = "SELECT USERNAME DBUSER,ACCOUNT_STATUS STATUS,LOCK_DATE LDATE,EXPIRY_DATE EDATE FROM dba_users"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        lst = []
        for i in res:
            lst.append({'DBUSER':i[0],'STATUS':i[1],'LDATE':i[2],'EDATE':i[3]})
        LOG.debug("Sql: %s,Result: %s", sql, str(lst), extra={"monitor": 'oracle', "modulo": "user_status"})
        return lst

    def user_status(self, dbuser):
        """Determines whether a user is locked or not"""
        sql = "SELECT USERNAME DBUSER,ACCOUNT_STATUS STATUS,LOCK_DATE LDATE,EXPIRY_DATE EDATE FROM dba_users WHERE username='{0}'".format(dbuser)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for i in res:
            LOG.debug("Sql: %s,Result: %s",sql, str(i[0]), extra={"monitor": 'oracle', "modulo": "user_status"})
            return {'DBUSER':i['DBUSER'],'STATUS':i['STATUS'],'LDATE':i['LDATE'],'EDATE':i['EDATE']}
        return None

    def __init__(self,persistent=False,tnsnames=None,username=None,password=None,address=None,port=None,sid=None,**kwargs):
        self.persistent = persistent
        self.tnsnames = tnsnames
        self.username = username
        self.password = password
        self.address = address
        self.port = port
        self.sid = sid
        self.db = None
        self.cur = None

    def db_connect(self):
        if not self.persistent or self.db is None:
            username = self.username
            password = self.password
            address = self.address if self.address else '127.0.0.1'
            sid = self.sid if self.sid else 'orcl'
            port = self.port if self.port else 1521
            #TODO CONNECTAR POR TNSNAMES
            self.db = cx_Oracle.connect("{0}/{1}@{2}:{3}/{4}".format(username, password, address, port, sid))
            self.cur = self.db.cursor()

    def db_close(self,force=False):
        if self.cur and force:
            self.cur.close()
        if self.db and force:
            self.db.close()

    def version2(self):
        return self.db.version

    def execute(self, func,force=False, **kwargs):
        ret = []
        try:
            method = getattr(self, func)
            self.db_connect()
            ret = method(**kwargs)
        except Exception as e:
            LOG.error("Error %s", str(e), extra={"monitor": 'oracle', "modulo": func})
        finally:
            self.db_close(force=force)
        return ret