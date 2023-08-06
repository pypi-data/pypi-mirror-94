import binascii
from logging import getLogger
import os
import json
import hashlib
import time
import csv
import inspect
import sys
from m360.base.lib.gcparser import GCParser
import urllib2

LOG = getLogger('m360.base')

class Manager:

    APACHE_METHODS = ["GET","HEAD","POST"]
    ACCESS_LOG_WORDS_BLACKLIST = ["GET /health" , "GET /server-status","GET /manager/text/serverinfo","GET /manager/text/serverinfo"]

    TIME = "usegs"
    HITS = "hits"
    AGENT = "agent"
    HTTPCODE = "httpcode"
    METHOD = "method"
    BYTES = "bytes"
    ALLOWED_METRICS = [BYTES, TIME, HTTPCODE, HITS, METHOD]

    MAX_ACCESSLOG_WINDOW_SIZE = 1024 * 1024 * 400 #MB maximo tamano a procesar

    @staticmethod
    def getcaller():
        try:
            frame=inspect.stack()[2][0]
            instance=frame.f_locals['self']
            monitor=instance.tech
            modulo=""
            return {"monitor":monitor,"modulo":modulo}
        except:
            return {"monitor":"","modulo":""}

    @staticmethod
    def readwatchedfiles(logfiles,instance,**kwargs):
        arrstats = []
        if 'extractfunc' not in kwargs:
            return arrstats
        extractfunc=kwargs['extractfunc']
        prelinefunc=None
        if 'prelinefunc'  in kwargs:
            prelinefunc = kwargs['prelinefunc']
        summarize=True
        if 'summarize' in kwargs:
            summarize = kwargs['summarize']

        multiline=False
        if 'multiline' in kwargs:
            multiline = kwargs['multiline']

        for logtupla in logfiles:
            if not os.path.isfile(logtupla['log']) or not os.access(logtupla['log'], os.R_OK):
                LOG.error("[%s] No se puede leer el fichero (%s).", instance.name,logtupla['log'],extra={'monitor': instance.tech, 'modulo': 'access'})
                continue
            inode=os.stat(logtupla['log']).st_ino
            with open(logtupla['log']) as f:
                FIRSTBYTESSIZE=1024
                firstbytes=f.read(FIRSTBYTESSIZE)
                try:
                    firstbytes=firstbytes.decode('ascii')
                except Exception as e:
                    LOG.warning("[%s] No se puede leer los primeros bytes ASCII del fichero (%s).", instance.name,logtupla['log'],extra={'monitor': instance.tech, 'modulo': 'access'})
                    firstbytes=binascii.hexlify(firstbytes)
                # si el fichero esta vacio
                if sys.getsizeof(firstbytes)<FIRSTBYTESSIZE:
                    LOG.warning("[%s] Fichero (%s) menor de "+str(FIRSTBYTESSIZE)+" bytes.", instance.name, logtupla['log'],extra={'monitor': instance.tech, 'modulo': 'access'})
                    continue

                indexfilename=hashlib.md5(str(inode)+instance.name+logtupla['log']+instance.host+firstbytes).hexdigest()
                baseindexfilename=None
                if 'lognamepattern' in logtupla:
                    baseindexfilename=os.path.join(instance.getindexpath(),
                                                   hashlib.md5(instance.name+
                                                               logtupla['lognamepattern']+
                                                               instance.host).hexdigest()+'.idx')

                if not os.path.isfile(os.path.join(instance.getindexpath(),indexfilename+'.idx')):
                    cursor=0
                    stats = {} if summarize else []
                    #traemos las acumuladas del log anterior si existe
                    if baseindexfilename and os.path.isfile(baseindexfilename):
                        try:
                            with open(baseindexfilename,'r') as f2:
                                LOG.debug("[%s] Leyendo Fichero index padre (%s) para (%s).", instance.name,
                                              baseindexfilename, logtupla['log'],
                                              extra={'monitor': instance.tech, 'modulo': 'access'})
                                metadata=json.loads(f2.read())
                                if summarize:
                                    #TODO: controlar OVERFLOW
                                    stats=metadata['stats']
                                else:
                                    stats=[]
                        except Exception as e:
                            os.remove(os.path.join(instance.getindexpath(),indexfilename+'.idx'))
                            LOG.error("[%s] Parseando json Fichero index padre (%s) para (%s).", instance.name,
                                          baseindexfilename,
                                          logtupla['log'], extra={'monitor': instance.tech, 'modulo': 'access'})
                else:
                    try:
                        with open(os.path.join(instance.getindexpath(),indexfilename+'.idx'),'r') as f2:
                            LOG.debug("[%s] Leyendo Fichero index (%s) para (%s).", instance.name,os.path.join(instance.getindexpath(),indexfilename+'.idx'), logtupla['log'],extra={'monitor': instance.tech, 'modulo': 'access'})
                            metadata=json.loads(f2.read())
                            cursor=metadata['cursor']
                            if summarize:
                                stats=metadata['stats']
                            else:
                                stats=[]
                    except Exception as e:
                        os.remove(os.path.join(instance.getindexpath(),indexfilename+'.idx'))
                        LOG.error("[%s] Parseando json Fichero index (%s) para (%s).", instance.name,
                                      os.path.join(instance.getindexpath(), indexfilename + '.idx'),
                                      logtupla['log'], extra={'monitor': instance.tech, 'modulo': 'access'})
                        cursor = 0
                        stats = {} if summarize else []
                ##WORKAROUND TSB
                ##SI EL FICHERO ES MUY GRANDE PASAMOS DE LEERLO Y ACTUALIZAMOS SOLO EL CURSOR DESDE EL FINAL
                f.seek(0,os.SEEK_END)
                pos=f.tell()
                #BUG: Por algun motivo, el cursor guardado es mayor que el tamanno del fichero
                #Leemos desde el principio
                if (cursor>pos):
                    LOG.warning("[%s] El cursor anterior es mayor que el tamanno del fichero '%s'. (%d > %d).", instance.name,logtupla['log'],cursor,pos,extra={'monitor': instance.tech, 'modulo': 'access'})
                    cursor=0
                    #TODO: traemos las acumuladas del log anterior si existe
                    #TODO: controlar OVERFLOW

                if (pos-cursor)>Manager.MAX_ACCESSLOG_WINDOW_SIZE:
                    LOG.warning("[%s] New file logs lines (%s) too big (%d MB). Skipping.",instance.name,logtupla['log'],int((pos-cursor)/(1024*1024)),extra={'monitor':instance.tech,'modulo':'access'})
                    cursor=pos
                else:
                    f.seek(cursor,0)
                    timexecute=time.time()
                    LOG.info("[%s] Parsing %d Bytes window of file %s", instance.name, long(pos - cursor),
                                 logtupla['log'],extra={'monitor':instance.tech,'modulo':'access'})

                    old_cursor=cursor
                    while(cursor<pos):
                        if multiline:
                            line = f.readlines()
                        else:
                            line = f.readline()
                        if prelinefunc:
                            line = prelinefunc(line,logtupla)
                        if line:
                            #acumulados
                            stats = extractfunc(line,instance,logtupla,stats)
                            #no acumulados
                        cursor=f.tell()
                    LOG.info("[%s] Parsed %d bytes file (%s) in %.3f seg.", instance.name,pos - old_cursor,
                                 logtupla['log'],time.time()-timexecute,extra={'monitor':instance.tech,'modulo':'access'})

            #SI NO HAY METRICAS NO METEMOS EL VHOST
            if stats and summarize:
                stats['vhost']=logtupla['host']

            #V2 metricas de accessos
            statsV2 = []
            if summarize:
                l_hits = stats['hits'] if 'hits' in stats else 0
                for metrica,count in stats.items():
                    if metrica.startswith("http_"):
                        newmetric={'count:V2':count,
                                   'httpcode:V2':metrica.replace("http_","")+"RC",
                                   'hits:V2':l_hits
                                   }
                        if summarize:
                            newmetric['vhost']=logtupla['host']
                        statsV2.append(newmetric)

            with open(os.path.join(instance.getindexpath(),indexfilename)+'.idx','w') as f2:
                json.dump({'cursor':cursor,'stats':stats if summarize else {}}, f2)

            if baseindexfilename:
                with open(baseindexfilename,'w') as f2:
                    json.dump({'lastprocesed':logtupla['log'],'stats':stats if summarize else {}}, f2)

            if logtupla['outputmetrics']:
                arrstats.extend(statsV2)
                if summarize:
                    arrstats.append(stats)
                else:
                    arrstats.extend(stats)

        return arrstats


    @staticmethod
    def getaccessmetrics(instance):
        arrstats = []
        logfiles = instance.getlogfiles()
        if not logfiles:
            LOG.warning("[%s] No se ha obtenido el nombre del fichero de acccesos.", instance.name,extra={'monitor':instance.tech,'modulo':'access'})
            return arrstats

        return Manager.readwatchedfiles(logfiles,instance,extractfunc=Manager.updatestats,
                                        prelinefunc=Manager.linetocvs,summarize=True)

    @staticmethod
    def linetodict(line,logtupla):
        #line_parser = apache_log_parser.make_parser(logtupla['format'])

        log_line_data = None
        try:
            #log_line_data = line_parser(line)
            pass
        except Exception as e:
            LOG.error("Error parseando linea: %e", e.message,extra={'monitor':'NA','modulo':'access'})

        return log_line_data

    @staticmethod
    def linetocvs(line,logtupla):
        l_aux=None

        #TODO: DESCARTAMOS LINEAS QUE TENGAN CADENAS BLACKLIST
        for wbl in Manager.ACCESS_LOG_WORDS_BLACKLIST:
            if line.find(wbl)>=0:
                return l_aux

        # BUG WEBLOGIC ACCESS FILE
        if not line.strip().startswith("#"):
            #JUNTAMOS LAS LISTAS DE IPs
            if logtupla['format'].lower().find("x-forwarded")>=0 or logtupla['format'].lower().find("ip-client")>=0:
                line=line.replace(", ","_")
            sep=' '
            if 'separator' in logtupla:
                sep=logtupla['separator']
                if len(sep)>1:
                    line=line.replace(sep,"|")
                    sep='|'
            line=line.strip()
            reader = csv.reader([line.replace('[', '"').replace(']', '"').replace("\t", " ")], delimiter=str(sep),skipinitialspace=True)
            try:
                l_aux = reader.next()
            except Exception as e:
                LOG.warning("Error parseando CVS (%s). Error: %s",logtupla['log'],e.message,extra={'monitor': "NA", 'modulo': 'access'})

        return l_aux

    @staticmethod
    def getGCmetrics(instance):
        arrstats = []
        logfiles = instance.getgcfiles()
        if not logfiles:
            LOG.warning("[%s] No se ha obtenido el nombre del fichero GC.", instance.name,extra={'monitor':instance.tech,'modulo':'access'})
            return arrstats

        return Manager.readwatchedfiles(logfiles,instance,
                                        extractfunc=Manager.updateGCstats,
                                        summarize=False,
                                        multiline=True)

    @staticmethod
    def updateGCstats(lines,instance,loginfo,stats):
        try:
            stats.extend(GCParser.parse(lines,start=instance.starttime,gcoptions=loginfo['gcoptions']))
        except Exception as e:
            pass

        return stats

    @staticmethod
    def updatestatsdict(linearray, instance, loginfo, stats):
        if Manager.HTTPCODE in Manager.ALLOWED_METRICS:
            try:
                if "status" in linearray:
                    status = linearray["status"]
                    statusAux = int(status)
                    if statusAux >= 200 and statusAux <= 599:
                        stats["http_" + status] = stats["http_" + status] + 1 if "http_" + status in stats else 1
                    else:
                        LOG.debug("[%s] Dato no calculado: %s, error:%s", instance.name, Manager.HTTPCODE,
                                      str(statusAux) + " no es un codigo de estado valido",
                                      extra={'monitor': instance.tech, 'modulo': 'access'})
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s", instance.name, Manager.HTTPCODE, e.message,
                              extra={'monitor': instance.tech, 'modulo': 'access'})

        if Manager.TIME in Manager.ALLOWED_METRICS:
            try:
                # %{s}T=%T,%{us}T=%D,%{ms}T
                factor = 1
                time = 0
                if "time_us" in linearray:
                    # Microsegundos
                    time = float(linearray["time_us"])
                elif "time_s" in linearray:
                    # Segundos
                    factor = 1000000
                    time = float(linearray["time_s"])
                elif "time_ms" in linearray:
                    # Milisegundos
                    factor = 1000
                    time = float(linearray["time_ms"])
                if time > 0:
                    stats[Manager.TIME] = stats[Manager.TIME] + time * factor if Manager.TIME in stats else time * factor
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s", instance.name, Manager.TIME, e.message,
                              extra={'monitor': instance.tech, 'modulo': 'access'})

        if Manager.METHOD in Manager.ALLOWED_METRICS:
            try:
                method = ""
                if "request_first_line" in linearray:
                    method = linearray["request_first_line"].split()[0].replace("/", "")
                elif "method" in linearray:
                    method = linearray["method"]
                if method in Manager.APACHE_METHODS:
                    stats[method] = stats[method] + 1 if method in stats else 1
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s", instance.name, Manager.METHOD, e.message,
                              extra={'monitor': instance.tech, 'modulo': 'access'})

        if Manager.BYTES in Manager.ALLOWED_METRICS:
            try:
                bytes = 0
                if "response_bytes_clf" in linearray:
                    bytes = int(linearray["response_bytes_clf"])
                elif "response_bytes" in linearray:
                    bytes = int(linearray["response_bytes"])
                stats[Manager.BYTES] = stats[Manager.BYTES] + bytes if Manager.BYTES in stats else bytes
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s", instance.name, Manager.BYTES, e.message,
                              extra={'monitor': instance.tech, 'modulo': 'access'})

        if Manager.AGENT in Manager.ALLOWED_METRICS:
            try:
                if "request_header_user_agent" in linearray:
                    agent = linearray["request_header_user_agent"]
                    stats[agent] = stats[agent] + 1 if agent in stats else 1
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s", instance.name, Manager.AGENT, e.message,
                              extra={'monitor': instance.tech, 'modulo': 'access'})

        if Manager.HITS in Manager.ALLOWED_METRICS:
            stats[Manager.HITS] = stats[Manager.HITS] + 1 if Manager.HITS in stats else 1

        return stats

    @staticmethod
    def updatestats(linearray,instance,loginfo,stats):
        #format = loginfo['format']
        '''
        keys24 = {  "%D": "The time taken to serve the request, in microseconds.",
                    "%a": "Client IP address of the request",
                    "%k": "Number of keepalive requests handled on this connection. Interesting if KeepAlive is being used, so that, for example, a '1' means the first keepalive request after the initial one, '2' the second, etc...; otherwise this is always 0 (indicating the initial request).",
                    "%q": "The query string",
                    "%T": "The time taken to serve the request, in seconds.",
                    "%{unit}T": "The time taken to serve the request, in unit %{s}T=%T,%{us}T=%D,%{ms}T",
                    "%h": "Remote host or IP",
                    "%r": "First line request. METHOD URI",
                    "%>s": "Final status",
                    "%s":  "Status",
                    "%b": "Size of response in bytes.",
                    "%{User-Agent}i": "User agent",
                    "%t": Fecha
        }'''

        keyposition=loginfo['keyposition']

        if len(keyposition)!=len(linearray):
            LOG.debug("[%s] Numero de indices de formato diferente al numero de columnas de log: (%d != %d)",
                          instance.name, len(keyposition),len(linearray),
                          extra={'monitor': instance.tech, 'modulo': 'access'})

        if Manager.HTTPCODE in Manager.ALLOWED_METRICS:
            try:
                status=linearray[keyposition.index("%s")]
                statusAux=int(status)
                if statusAux>=200 and statusAux<=599:
                    stats["http_"+status]= stats["http_"+status] +1 if "http_"+status in stats else 1
                else:
                    LOG.debug("[%s] Dato no calculado: %s, error:%s", instance.name, Manager.HTTPCODE,str(statusAux)+" no es un codigo de estado valido",extra={'monitor':instance.tech,'modulo':'access'})
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s",instance.name,Manager.HTTPCODE,e.message,extra={'monitor':instance.tech,'modulo':'access'})

        if Manager.TIME in Manager.ALLOWED_METRICS:
            try:
                # %{s}T=%T,%{us}T=%D,%{ms}T
                factor=1
                time=0
                if "%D" in keyposition or "%{us}T" in keyposition:
                    #Microsegundos
                    time = float(linearray[keyposition.index("%D")])
                elif "%T" in  keyposition or "%{s}T" in keyposition:
                    #Segundos
                    factor=1000000
                    time = float(linearray[keyposition.index("%T")])
                elif "%{ms}T" in  keyposition:
                    #Milisegundos
                    factor=1000
                    time = float(linearray[keyposition.index("%D")])
                if time > 0:
                    stats[Manager.TIME] = stats[Manager.TIME] + time*factor if Manager.TIME in stats else time*factor
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s",instance.name,Manager.TIME,e.message,extra={'monitor':instance.tech,'modulo':'access'})


        if Manager.METHOD in Manager.ALLOWED_METRICS:
            try:
                method = ""
                if "%r" in keyposition:
                    method = linearray[keyposition.index("%r")].split()[0].replace("/", "")
                elif "%m" in keyposition:
                    method = linearray[keyposition.index("%m")]
                if method in Manager.APACHE_METHODS:
                    stats[method] = stats[method] + 1 if method in stats else 1
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s",instance.name,Manager.METHOD,e.message,extra={'monitor':instance.tech,'modulo':'access'})

        if Manager.BYTES in Manager.ALLOWED_METRICS:
            try:
                bytes = int(linearray[keyposition.index("%b")])
                stats[Manager.BYTES] = stats[Manager.BYTES] + bytes if Manager.BYTES in stats else bytes
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s",instance.name,Manager.BYTES,e.message,extra={'monitor':instance.tech,'modulo':'access'})

        if Manager.AGENT in Manager.ALLOWED_METRICS:
            try:
                agent = linearray[keyposition.index("%{User-Agent}i")]
                stats[agent] = stats[agent] + 1 if agent in stats else 1
            except Exception as e:
                LOG.debug("[%s] Dato no calculado: %s, error:%s",instance.name,Manager.AGENT,e.message,extra={'monitor':instance.tech,'modulo':'access'})

        if Manager.HITS in Manager.ALLOWED_METRICS:
            stats[Manager.HITS]= stats[Manager.HITS]+1 if Manager.HITS in stats else 1

        return stats

    @staticmethod
    def url_alive(url):
        try:
            urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            return e.code == 401
        except urllib2.URLError, e:
            return False
        return True
