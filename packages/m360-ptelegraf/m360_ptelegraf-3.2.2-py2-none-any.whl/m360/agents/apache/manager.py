import re
from logging import getLogger
import m360.base.manager as base
import urllib2
import socket
true_socket = socket.socket

LOG=getLogger('m360.agents.apache')

def make_bound_socket(source_ip):
    def bound_socket(*a, **k):
        sock = true_socket(*a, **k)
        sock.bind((source_ip, 0))
        return sock
    return bound_socket


class Manager (base.Manager):

    APACHE_METHODS = ["GET","HEAD","POST"]

    TIME = "usegs"
    HITS = "hits"
    AGENT = "agent"
    HTTPCODE = "httpcode"
    METHOD = "method"
    BYTES = "bytes"
    ALLOWED_METRICS = [BYTES, TIME, HTTPCODE, HITS, METHOD]

    MAX_ACCESSLOG_WINDOW_SIZE = 1024 * 1024 * 400 #MB maximo tamano a procesar

    @staticmethod
    def status(endpoint):
        res={}

        try:
            #Python puede que no este compilado con SSL
            #Depende de las librerias de SO openssl-dev
            import ssl
            socket.socket = make_bound_socket('127.0.0.1')
            conn = urllib2.urlopen('{}?auto'.format(endpoint),timeout=3,context=ssl._create_unverified_context())
            if conn.code!=200 or conn.headers.type!="text/plain":
                return res
            res['code']=conn.code
            response = conn.read()
            conn.close()
            for line in response.split("\n"):
                if ':' in line:
                    linesplitted = line.split(':')
                    if len(linesplitted)==2:
                        key, value=linesplitted[:2]
                        if key == 'Scoreboard':
                            res['scoreboard']=Manager.parsescoreboard(value.strip())
                        else:
                            if key in [ 'ServerVersion' ]:
                                res[key]=value.strip().replace(' ', '')
                            else:
                                if 'status' not in res:
                                    res['status'] = {}
                                res['status'][key.strip().replace(' ','')]=value.strip().replace(' ', '_')
        except urllib2.HTTPError as e:
            LOG.error("Error getting URL %s: %d %s",endpoint,e.code,e.msg,extra=Manager.getcaller())
            res['code']=e.code
        except Exception as e2:
            LOG.error("Error getting URL %s: Unexpected error %s",endpoint ,e2.message,extra=Manager.getcaller())
        finally:
            socket.socket = true_socket

        return res

    @staticmethod
    def parsescoreboard(str):
        """ Parses scoreboard """
        keys = {
            '_': 'WaitingForConnectionWorkers',
            'S': 'StartingUpWorkers',
            'R': 'ReadingRequestWorkers',
            'W': 'SendingReplyWorkers',
            'K': 'KeepaliveReadWorkers',
            'D': 'DNSLookupWorkers',
            'C': 'ClosingConnectionWorkers',
            'L': 'LoggingWorkers',
            'G': 'GracefullyFinishingWorkers',
            'I': 'IdleWorkers',
            '.': 'OpenSlotWorkers'
        }

        scores = {
            'StartingUpWorkers':0,
            'ReadingRequestWorkers':0,
            'SendingReplyWorkers':0,
            'KeepaliveReadWorkers':0,
            'DNSLookupWorkers':0,
            'ClosingConnectionWorkers':0,
            'WaitingForConnectionWorkers':0,
            'LoggingWorkers':0,
            'GracefullyFinishingWorkers':0,
            'IdleWorkers':0,
            'OpenSlotWorkers':0
        }

        maxWorkers=0
        for score in str:
            maxWorkers+=1
            if keys[score] in scores:
                scores[keys[score]] += 1
            else:
                scores[keys[score]] = 1

        scores["maxWorkers"] = maxWorkers
        return scores

    @staticmethod
    def parseconf(conffile, accesslog="", formatlogs=None, formatname=""):
        ##BUSCAMOS EL LOG DE ACCESOS
        if formatlogs is None:
            formatlogs = {}
        includes=[]
        with open(conffile, 'r') as f:
            lines=f.readlines()
            for line in lines:
                if line[0]=="#":
                    continue

                ##Guardamos los includes
                matches = re.findall('^\s*Include\s+\"?([^\"\s]+)\"?\s*', line)
                if len(matches)>0:
                    includes.append(matches[0])

                if accesslog=="":
                    matches = re.findall('^\s*CustomLog\s+\"?([^\"\s]+)\"?\s+([^\s]+)?', line)
                    if len(matches)>0:
                        accesslog=matches[0][0]
                        if len(matches[0])>1:
                            formatname=matches[0][1]
                            if formatname in formatlogs:
                                return [accesslog,formatlogs,formatname]
                            else:
                                continue
                        else:
                            return [accesslog,{},""]

                matches = re.findall('^\s*LogFormat\s+\"(.+)\"\s+([^\s]+)\s+', line)
                if len(matches)>0:
                    formatlogs[matches[0][1]]=matches[0][0]

        if formatname != "" and formatname in formatlogs:
            return [accesslog,formatlogs,formatname]

        for newconffile in includes:
            accesslog, formatlogs,formatname=Manager.parseconf(newconffile,accesslog,formatlogs,formatname)
            if (accesslog!=""):
                if(formatname!=""):
                    if formatname in formatlogs:
                        return [accesslog, formatlogs, formatname]
                else:
                    return [accesslog, formatlogs, formatname]

        return [accesslog,formatlogs,formatlogs]

    @staticmethod
    def processLine(self,line,args):
        return self.updatestats(line,args['instance'],args['format'], args['stats'])


    @staticmethod
    def summarize(arrstags):
        stats = {}
        for stat in arrstags:
            for key in stat.keys():
                stats[key] = stats[key] + stat[key] if key in stats else stat[key]
        return stats
