import copy
import platform
from m360.base.lib.myparseapacheconfig import myParseApacheConfig as myParse
from pyparsing import ParseException
from collections import defaultdict,namedtuple
import re
from datetime import timedelta
import datetime,time
import collections
import json
import subprocess
from logging import getLogger
import os
from m360.base.settings import Settings
import hashlib

LOG=getLogger('m360.base.lib')

class ServiceExit(Exception): pass

class Utils(object):

    @staticmethod
    def majorversion(ver_str):
        return "1.8"

    @staticmethod
    def addkeyprefix(d,prefix):
        retdict = {}
        for key,val in d.iteritems():
            retdict[prefix+key] = val
        return retdict

    @staticmethod
    def linux_distribution():
      try:
        return platform.linux_distribution()
      except:
        return "N/A"

    @staticmethod
    def toDict(a):
        ret={}
        if isinstance(a,dict):
            return a
        for name, value in a._asdict().items():
            ret[name]=value
        return ret

    @staticmethod
    def getDirectiveValue(directive,apache_conf,multiple=False,basepath=""):
        rets = []
        for i in apache_conf:
            if myParse.isComment(i):
                continue
            if myParse.isNestedTags(i):
                #NO SE SOPORTAN VHOSTS
                if i.open_tag.lower().find("virtualhost")==-1:
                    retaux = Utils.getDirectiveValue(directive,i,multiple=multiple,basepath=basepath)
                    if retaux:
                        if multiple:
                            rets.extend(retaux)
                        else:
                            return retaux
            elif myParse.isDirective(i):
                if i.name.upper() == directive.upper():
                    if not multiple:
                        return i.args
                    else:
                        rets.append(i.args)
                elif i.name.upper() == "INCLUDE":
                    try:
                        print("Parseando el fichero " + basepath+"/"+i.args)
                        apache_parse_obj = myParse(basepath + "/" + i.args)
                        apache_conf2 = apache_parse_obj.parse_config()
                        retaux = Utils.getDirectiveValue(directive, apache_conf2, multiple=multiple, basepath=basepath)
                        if retaux:
                            if multiple:
                                rets.extend(retaux)
                            else:
                                return retaux
                    except ParseException as e:
                        print "No se pudo parsear el fichero " + basepath+"/"+i.args + " Linea:" + e.line
                    except Exception as e:
                        print "No se pudo parsear el fichero " + basepath+"/"+i.args + " Error:" + e.message

        return rets if multiple else ""

    @staticmethod
    def grep(strstream,val):
        return "\n".join([r for r in strstream.split("\n") if re.search(val,r, re.IGNORECASE)])


    @staticmethod
    def etree_to_dict(t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(Utils.etree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            for k, v in dd.items():
                if len(v) == 1:
                    d[t.tag][k] = v[0]
                else:
                    d[t.tag][k] = v
        if t.attrib:
            d[t.tag].update((k, v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d

    @staticmethod
    def safeval(arr,val):
        if val in arr:
            return arr[val]
        else:
            return None

    @staticmethod
    def dict2namedtuple(thedict, name):
        thenametuple = namedtuple(name, [])
        for key, val in thedict.items():
            if not isinstance(key, str) and not isinstance(key, unicode):
                msg = 'dict keys must be strings not {}'
                raise ValueError(msg.format(key.__class__))

            if not isinstance(val, dict):
                setattr(thenametuple, key, val)
            else:
                newname = Utils.dict2namedtuple(val, key)
                setattr(thenametuple, key, newname)

        return thenametuple

    @staticmethod
    def merge_two_dicts(x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z

    @staticmethod
    def contains(array, str):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        for i in array:
            if i.find(str)>=0:
                return True
        return False

    @staticmethod
    def dict_populate(dct,attrs=None):
        ret = {}
        if attrs is None:
            return copy.deepcopy(dct)
        for a in attrs:
            if a in dct:
                ret[a] = copy.deepcopy(dct[a])
        return ret


    @staticmethod
    def dict_merge(dct, merge_dct):
        """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
        updating only top-level keys, dict_merge recurses down into dicts nested
        to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
        ``dct``.
        :param dct: dict onto which the merge is executed
        :param merge_dct: dct merged into dct
        :return: None
        """
        for k, v in merge_dct.iteritems():
            if (k in dct and isinstance(dct[k], dict)
                    and isinstance(merge_dct[k], collections.Mapping)):
                Utils.dict_merge(dct[k], merge_dct[k])
            else:
                dct[k] = merge_dct[k]

    @staticmethod
    def convertDate(strval):
        #%Y-%m-%d_%H
        now = datetime.datetime.today()
        month = str(now.month) if now.month > 9 else "0"+ str(now.month)
        day = str(now.day) if now.day > 9 else "0" + str(now.day)
        hour = str(now.hour) if now.hour > 9 else "0" + str(now.hour)
        return strval.replace("%Y",str(now.year)).replace("%m",month).replace("%d",day).replace("%H",hour)


    @staticmethod
    def previousRotateFile(strval,instance):
        previousfile=None
        lastprocesed=''
        #%Y-%m-%d_%H
        #COMPROBAR SI EL FICHERO ANTERIOR YA SE HA PROCESADO ENTERO
        baseindexfilename=os.path.join(instance.getindexpath(),hashlib.md5(instance.name+strval+instance.host).hexdigest()+'.idx')
        if not os.path.isfile(baseindexfilename):
            return None
        else:
            try:
                with open(baseindexfilename,'r') as f:
                    metadata=json.loads(f.read())
                    lastprocesed=metadata['lastprocesed']
                    if not lastprocesed:
                        return None
            except Exception as e:
                LOG.error("getting previousRotateFile. {}".format(str(e)),
                          extra={'monitor':'None','module':'Access'})
                return None

        now = datetime.datetime.today()
        nmonth = str(now.month) if now.month > 9 else "0"+ str(now.month)
        nday = str(now.day) if now.day > 9 else "0" + str(now.day)
        nhour = str(now.hour) if now.hour > 9 else "0" + str(now.hour)
        if strval.find("%H")>=0:
            #SI EXISTE EL FICHERO EN CACHE. EL ANTERIOR YA FUE PROCESADO
            prev = now - timedelta(hours=1)
            month = str(prev.month) if prev.month > 9 else "0"+ str(prev.month)
            day = str(prev.day) if prev.day > 9 else "0" + str(prev.day)
            hour = str(prev.hour) if prev.hour > 9 else "0" + str(prev.hour)
            nowfile = strval.replace("%Y",str(now.year)).replace("%m",nmonth).replace("%d",nday).replace("%H",nhour)
            previousfile = strval.replace("%Y",str(prev.year)).replace("%m",month).replace("%d",day).replace("%H",hour)
            if nowfile==lastprocesed or nowfile==previousfile:
                return None
        elif strval.find("%d")>=0:
            prev = now - timedelta(hours=1)
            month = str(prev.month) if prev.month > 9 else "0"+ str(prev.month)
            day = str(prev.day) if prev.day > 9 else "0" + str(prev.day)
            nowfile = strval.replace("%Y",str(now.year)).replace("%m",nmonth).replace("%d",nday)
            previousfile = strval.replace("%Y",str(prev.year)).replace("%m",month).replace("%d",day)
            if nowfile==lastprocesed or nowfile==previousfile:
                return None

        return previousfile

    @staticmethod
    def printobj(obj):
        print json.dumps({'object':obj})


    @staticmethod
    def runcmd(cmd,roottag="body",monitor="NA",modulo="NA",jsonmode=True):
        #TODO:  Desde aqui se llamaran a los comandos de sistema operativo
        #       comprobar que el comando no se esta ejecutando
        #       si ha pasado mas de X segundos, matamos y lo lanzamos
        #       Logger.debug del comando
        # returns output as byte string
        LOG.debug("Executing %s", cmd, extra={"monitor": monitor, "modulo": modulo})
        dataaux2 = {'mensaje':""}
        try:
            returned_output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT, universal_newlines=True)
            if jsonmode:
                dataaux2 = json.loads(Utils.grep(returned_output, roottag))
            else:
                dataaux2['body']={'item':{}}
                dataaux3 = returned_output.split("\n")
                for i in dataaux3:
                    stringg = i.strip()
                    if stringg.startswith("MBeanName") or stringg.startswith("Weblogic XMLX Module"):
                        continue
                    if stringg.find(":")<0:
                        continue
                    arrayvals = stringg.split(":")
                    dataaux2['body']['item'][arrayvals[0]]="".join(arrayvals[1:]).strip()

            LOG.debug("Successful (%s) Executed %s",dataaux2['mensaje'], cmd,
                                      extra={"monitor": monitor, "modulo": modulo})
        except subprocess.CalledProcessError as e:
            errmsg=Utils.grep(e.output, "exception")
            LOG.error("Executed: %s ERRCODE: %s ERRMSG: %s", cmd, e.returncode,errmsg,
                                        extra={"monitor": monitor, "modulo": modulo})
            dataaux2['mensaje'] = "Error {},Msg:{}".format(e.returncode,errmsg)
        except Exception as e:
            LOG.error("Error %s", e.message, extra={"monitor": monitor, "modulo": modulo})
            dataaux2['mensaje'] = "Error {}".format(e.message)

        return dataaux2

    #REVISAMOS QUE EN EL FORMATO DE UN LOG LO QUE VA ENTRE ESTOS CARACTERES SOLO PUEDE TENER UN FORMATO
    @staticmethod
    def parselogformat(format):
        #eliminamos los %{loquesea}%t y lo sustituimos por %t
        f = re.sub(r'%{[^}]+}t', '%t', format)

        f = re.sub(r'\[[^%]*(%({[^}]+})?.).*\]', r'[\1]', f)

        f = re.sub(r'"[^%]*(%({[^}]+})?.)[^"]*"', r'"\1"', f)

        if f.find("%r") >= 0:
            if f.find("\"%r\"") == -1:
                f = f.replace('%r', '%r %r_uri %r_protocol')

        return f

    @staticmethod
    def logseparator(format):
        sep=" "
        arrvals=format.split("%")
        counting={}
        max=0
        for i in arrvals:
            line = re.sub(r'[A-Za-z\>\"\}\{]','',i)
            if line not in counting:
                counting[line]=1
            else:
                counting[line] = counting[line] + 1
            if counting[line]>max:
                sep=line
                max=counting[line]
        return sep

    @staticmethod
    def keyposition(format,sep=" "):
        if format == "":
            keyposition = ["%h", "%l", "%u", "%t", "%r", "%s", "%b"]
        else:
            keyposition = format.replace('"', '').replace("'", '').replace('\\', ''). \
                replace(">", '').replace("[", '').replace("]", '').split(sep)
        return keyposition

    @staticmethod
    def parseWLlogformat(format):
        f = format.replace('cs-method','%m').\
            replace("sc-status","%s").\
            replace("cs-uri","%U").\
            replace("cs-uri-query","%q").\
            replace("time-taken","%T").\
            replace("bytes","%b")
        return f

    @staticmethod
    def kill(pid):
        os.kill(int(pid), 9)
        return True

    #FORMATO DE SALIDA:
    # "TAG1=string1,TAG2=string2,.....,TAGn=stringN",campo1=Float1,campo2=Float2,...,<UNIXTIMESTAMP>
    # EL TIMESTAMP ES OPCIONAL, sino existe se recupera la fecha de sistema
    # LOS TAGS TIENEN QUE IR ENTRE COMILLAS, NO ES NECESARIO NI EL HOST, NI LA INSTANCIA
    @staticmethod
    def runcustomcmd(cmd,roottag="customdata",monitor="NA",modulo="NA",jsonmode=True):
        dataaux2 = {'mensaje':"",'body':{'items':[]}}

        #obtenemos un ID para guardar el PID
        if not os.path.isdir(Settings.MONITOR_CACHE):
            os.mkdir(Settings.MONITOR_CACHE)
        if not os.path.isdir(os.path.join(Settings.MONITOR_CACHE,'pids')):
            os.mkdir(os.path.join(Settings.MONITOR_CACHE,'pids'))

        pidfile=os.path.join(Settings.MONITOR_CACHE,'pids',hashlib.md5(cmd).hexdigest())
        if os.path.isfile(pidfile):
            #VEMOS SI SIGUE EJECUTANDOSE
            with open(pidfile,'r') as f:
                pid=f.read()
            secsfromstart=Utils.isrunning(pid)
            if secsfromstart:
                if secsfromstart>Settings.MAX_RUNNING_PROCESS:
                    LOG.warning("Command %s (PID:%s) max time (%s) reached. Killing.", cmd,pid,
                                                Settings.MAX_RUNNING_PROCESS,
                                                extra={"monitor": monitor, "modulo": modulo})
                    Utils.kill(pid)
                else:
                    #TODAVIA SE ESTA EJECUTANDO
                    LOG.info("Command %s (PID:%s) still running.", cmd,pid,
                                             extra={"monitor": monitor, "modulo": modulo})
                    return dataaux2
            else:
                #YA NO ESTA EJECUTANDOSE
                LOG.info("Command %s (PID:%s) dead.", cmd, pid,
                                         extra={"monitor": monitor, "modulo": modulo})
            os.remove(pidfile)


        LOG.debug("Executing %s", cmd, extra={"monitor": monitor, "modulo": modulo})
        try:
            proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
            pid = str(proc.pid)
            with open(pidfile,'w') as f:
                f.write(pid)
            returned_output = proc.communicate()[0]
            LOG.debug("Returned %s", returned_output, extra={"monitor": monitor, "modulo": modulo})

            ##            returned_output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT, universal_newlines=True)
            if jsonmode:
                dataaux2 = json.loads(Utils.grep(returned_output, roottag))
            else:
                dataaux3 = returned_output.split("\n")
                for i in dataaux3:
                    metrics={}
                    stringg = i.strip()
                    if stringg.startswith(roottag+":"):
                        stringg=stringg.replace(roottag+":","")
                    else:
                        m = re.search(r'([^:]+):',stringg)
                        if m:
                            level = m.group(1)
                            stringg = stringg.replace(level+":",'')
                            if level.lower() in dataaux2:
                                dataaux2[level.lower()].append(stringg)
                            else:
                                dataaux2[level.lower()] = [stringg]
                        continue
                    m = re.search(r'"([^"]+)"',stringg)
                    if m:
                        tags=m.group(1)
                        stringg = stringg.replace("\""+tags+"\"",'')
                        tagsarr=tags.strip().split(",")
                        for dupla in tagsarr:
                            aux=dupla.strip().split("=")
                            if len(aux)>1:
                                metrics[aux[0].strip()]=aux[1].strip()

                    fieldsarr=stringg.split(",")
                    for field in fieldsarr:
                        aux=field.strip()
                        if aux=="":
                            continue
                        auxarr=aux.split("=")
                        if len(auxarr)>1:
                            try:
                                metrics[auxarr[0].strip()] = float(auxarr[1].strip())
                            except Exception as e:
                                LOG.error("Field %s not valid float value (%s).",
                                                          auxarr[0].strip(),auxarr[1].strip(),
                                                          extra={"monitor": monitor, "modulo": modulo})
                        elif len(auxarr)==1:
                            timestamp=auxarr[0].strip()
                            if len(timestamp) == 10:
                                try:
                                    metrics["timestamp"] = int(timestamp)
                                except Exception as e:
                                    LOG.error("Timestamp %s not valid.",
                                                                timestamp,
                                                                extra={"monitor": monitor, "modulo": modulo})

                    dataaux2['body']['items'].append(metrics)

            os.remove(pidfile)
            LOG.debug("Successful (Lines returned: %d) Executed %s",len(dataaux2['body']['items']), cmd,
                                      extra={"monitor": monitor, "modulo": modulo})
        except subprocess.CalledProcessError as e:
            errmsg=Utils.grep(e.output, "exception")
            LOG.error("Executed: %s ERRCODE: %s ERRMSG: %s", cmd, e.returncode,errmsg,
                                        extra={"monitor": monitor, "modulo": modulo})
            dataaux2['mensaje'] = "Error {},Msg:{}".format(e.returncode,errmsg)
        except Exception as e:
            LOG.error("Error %s", str(e), extra={"monitor": monitor, "modulo": modulo})
            dataaux2['mensaje'] = "Error {}".format(str(e))

        return dataaux2

    @staticmethod
    def psfromhash(user,hash,monitor="NA",modulo="NA"):
        retpid=""
        cmd="ps axu | grep -v grep | grep "+user
        #obtenemos un ID para guardar el PID
        if not os.path.isdir(Settings.MONITOR_CACHE):
            os.mkdir(Settings.MONITOR_CACHE)
        if not os.path.isdir(os.path.join(Settings.MONITOR_CACHE,'pids')):
            os.mkdir(os.path.join(Settings.MONITOR_CACHE,'pids'))

        pidfile=os.path.join(Settings.MONITOR_CACHE,'pids',hashlib.md5(cmd).hexdigest())
        if os.path.isfile(pidfile):
            #VEMOS SI SIGUE EJECUTANDOSE
            with open(pidfile,'r') as f:
                pid=f.read()
            secsfromstart=Utils.isrunning(pid)
            if secsfromstart:
                if secsfromstart>Settings.MAX_RUNNING_PROCESS:
                    LOG.warning("Command %s (PID:%s) max time (%s) reached. Killing.", cmd,pid,
                                                Settings.MAX_RUNNING_PROCESS,
                                                extra={"monitor": monitor, "modulo": modulo})
                    Utils.kill(pid)
                else:
                    #TODAVIA SE ESTA EJECUTANDO
                    LOG.info("Command %s (PID:%s) still running.", cmd,pid,
                                             extra={"monitor": monitor, "modulo": modulo})
                    return retpid
            else:
                #YA NO ESTA EJECUTANDOSE
                LOG.info("Command %s (PID:%s) dead.", cmd, pid,
                                         extra={"monitor": monitor, "modulo": modulo})
            os.remove(pidfile)


        LOG.debug("Executing %s", cmd, extra={"monitor": monitor, "modulo": modulo})
        try:
            proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
            pid = str(proc.pid)
            with open(pidfile,'w') as f:
                f.write(pid)
            returned_output = proc.communicate()[0]
            LOG.debug("Returned %s", returned_output, extra={"monitor": monitor, "modulo": modulo})
            pslines=returned_output.split("\n")
            for psline in pslines:
                pslineclean=re.sub(r'\s+',' ',psline)
                pslinecleanarr=pslineclean.split(" ")
                cmdresult=" ".join(pslinecleanarr[10:])
                pshash=hashlib.md5(cmdresult).hexdigest()
                if pshash==hash:
                    retpid = pslinecleanarr[1]
                    break
            os.remove(pidfile)
        except subprocess.CalledProcessError as e:
            errmsg=Utils.grep(e.output, "exception")
            LOG.error("Executed: %s ERRCODE: %s ERRMSG: %s", cmd, e.returncode,errmsg,
                                        extra={"monitor": monitor, "modulo": modulo})
        except Exception as e:
            LOG.error("Error %s", str(e), extra={"monitor": monitor, "modulo": modulo})

        return retpid


    @staticmethod
    def parseColKeyVal(arr,translatecol=None,sep=' '):
        tablaret=[]
        if len(arr)>1:
            headerstr=arr[0].strip()
            headerstr = re.sub(r'\s+', ' ',headerstr)
            headers=headerstr.split(sep)
            for i in range(1,len(arr)):
                stripped=arr[i].strip()
                stripped=re.sub(r'\s+', ' ',stripped)
                if stripped!="":
                    values=stripped.split(sep)
                    newline={}
                    for j in range(min(len(values),len(headers))):
                        if translatecol:
                            key=headers[j]
                            if key in translatecol:
                                key=translatecol[key]
                                newline[key]=values[j].replace(",",".")
                    tablaret.append(newline)

        return tablaret

    @staticmethod
    def parseLineBlockCountExtract(arr,beginblock,endblock,extract):
        ret={}
        inblock=False
        for line in arr:
            stripped=line.strip()
            if not inblock:
                m=re.search(beginblock,stripped)
                if m:
                    inblock=True
            else:
                m=re.search(endblock,stripped)
                if m:
                    inblock=False
                else:
                    if stripped!="":
                        m=re.search(extract,stripped)
                        if m:
                            key=m.group(1)
                            if key in ret:
                                ret[key]=ret[key]+1
                            else:
                                ret[key]=1
                            inblock=False
        arrret=[]
        for idx,val in ret.iteritems():
            arrret.append({"count":val,"state":idx})
        return arrret

    @staticmethod
    def parseLineCountExtract(arr,find,extract):
        ret={}
        for line in arr:
            stripped=line.strip()
            if stripped!="":
                m=re.search(find,stripped)
                if m:
                    m=re.search(extract,stripped)
                    if m:
                        key=m.group(1)
                        if key in ret:
                            ret[key]=ret[key]+1
                        else:
                            ret[key]=1
        arrret=[]
        for idx,val in ret.iteritems():
            arrret.append({"count":val,"state":idx})
        return arrret


    @staticmethod
    def parseKeyVal(arr,sep='='):
        ret={}
        for i in arr:
            stripped=i.strip()
            if stripped=="VM Flags:":
                break
            if stripped!="":
                arri= stripped.split(sep)
                if len(arri)>1:
                    key=arri[0].strip()
                    val=sep.join(arri[1:])
                    if key!="":
                        ret[key]=val.strip()
        return ret

    @staticmethod
    def execute(cmd,formatFunc=None,monitor="NA",modulo="NA",extrapars=None):
        retlines=[]
        #obtenemos un ID para guardar el PID
        if not os.path.isdir(Settings.MONITOR_CACHE):
            os.mkdir(Settings.MONITOR_CACHE)
        if not os.path.isdir(os.path.join(Settings.MONITOR_CACHE,'pids')):
            os.mkdir(os.path.join(Settings.MONITOR_CACHE,'pids'))

        pidfile=os.path.join(Settings.MONITOR_CACHE,'pids',hashlib.md5(cmd).hexdigest())
        if os.path.isfile(pidfile):
            #VEMOS SI SIGUE EJECUTANDOSE
            with open(pidfile,'r') as f:
                pid=f.read()
            secsfromstart=Utils.isrunning(pid)
            if secsfromstart:
                if secsfromstart>Settings.MAX_RUNNING_PROCESS:
                    LOG.warning("Command %s (PID:%s) max time (%s) reached. Killing.", cmd,pid,
                                                Settings.MAX_RUNNING_PROCESS,
                                                extra={"monitor": monitor, "modulo": modulo})
                    Utils.kill(pid)
                else:
                    #TODAVIA SE ESTA EJECUTANDO
                    LOG.info("Command %s (PID:%s) still running.", cmd,pid,
                                             extra={"monitor": monitor, "modulo": modulo})
                    return retlines
            else:
                #YA NO ESTA EJECUTANDOSE
                LOG.info("Command %s (PID:%s) dead.", cmd, pid,
                                         extra={"monitor": monitor, "modulo": modulo})
            os.remove(pidfile)


        LOG.debug("Executing %s", cmd, extra={"monitor": monitor, "modulo": modulo})
        try:
            proc = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
            pid = str(proc.pid)
            with open(pidfile,'w') as f:
                f.write(pid)
            returned_output, output_err = proc.communicate()
            if proc.returncode:
                LOG.error("Cmd '%s' returned error %d. Stderr: %s",cmd,proc.returncode,
                                          output_err,extra={"monitor": monitor, "modulo": modulo})
            else:
                LOG.debug("Returned %s", returned_output, extra={"monitor": monitor, "modulo": modulo})
                retlines=returned_output.split("\n")
            os.remove(pidfile)
        except subprocess.CalledProcessError as e:
            errmsg=Utils.grep(e.output, "exception")
            LOG.error("Executed: %s ERRCODE: %s ERRMSG: %s", cmd, e.returncode,errmsg,
                                        extra={"monitor": monitor, "modulo": modulo})
        except Exception as e:
            LOG.error("Error %s", str(e), extra={"monitor": monitor, "modulo": modulo})
        extrapars2=extrapars if extrapars else {}
        return formatFunc(retlines,**extrapars2) if formatFunc else retlines

    @staticmethod
    def convert_interval(interval,unit="s"):
        if unit not in ["s","ms","us","ns"]:
            raise ServiceExit
        if interval.endswith(unit): ##TODO: ESTO ESTA MAL
            return int(interval.replace(unit,""))
        elif interval.endswith("d"):
            to_nseg = int(interval.replace("d", "")) * 1000000000 * 60 * 60 * 24
        elif interval.endswith("m"):
            to_nseg = int(interval.replace("m", "")) * 1000000000 * 60
        elif interval.endswith("h"):
            to_nseg = int(interval.replace("h", "")) * 1000000000 * 60 * 60
        else:
            to_nseg=interval.replace("ns","").replace("us","000").replace("ms","000000").replace("s","000000000")
        factor_nseg = unit.replace("ns","1").replace("us","1000").replace("ms","1000000").replace("s","1000000000")
        return float(int(to_nseg)/int(factor_nseg))
