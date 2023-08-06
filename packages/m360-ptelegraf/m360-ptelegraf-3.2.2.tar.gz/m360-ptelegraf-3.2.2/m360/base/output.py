import datetime
import time
from logging import getLogger
from importlib import import_module
from m360.base.telegraf_compat import get_tag_compat,get_field_compat,get_measurement_compat
import m360.base.settings as base
from m360.base.models import Timeseries
from m360.base.settings import Settings

LOG = getLogger('m360.base.output')


class OutputBase(object):
    def __init__(self,instance,conf=None):
        if conf is None:
            conf = {}
        self.conf = conf
        if "format" not in self.conf:
            self.conf['format'] = "influx"
        module = import_module("m360.formatter." + self.conf['format'])
        formatterObj = module.Formatter()
        self.formatter = formatterObj
        self.instance = instance

    def get_formatted_metrics(self,host,modulo,metricasobj):
        _formatted_metrics = []
        if metricasobj:
            now=datetime.datetime.now()
            if isinstance(metricasobj,Timeseries):
                for key,value in self.instance.get_global_tags().items():
                    metricasobj.add_global_tag(key,value)
                _formatted_metrics = self.formatter.format(metricasobj,instance=self.instance,host=host,modulo=modulo)
            else:
                version = metricasobj['ServerVersion'] if 'ServerVersion' in metricasobj else self.instance.getversion()
                if version is None or self.instance.technology not in Settings.TECHNOLOGY_WITH_VERSION:
                    version = ""
                if type(metricasobj) is list:
                    arrmetricas = metricasobj
                else:
                    arrmetricas = [metricasobj]

                for metricas in arrmetricas:
                    tags = {}
                    for key, value in self.instance.get_global_tags().items():
                        tags[key]=value
                    fields = {}
                    for key, val in metricas.items():
                        if key.find(":") >= 0:
                            key = key.split(":")[0]

                        if key != "timestamp" and type(val) not in [list, dict]:
                            if type(val) in [str, unicode]:
                                val2 = val
                                try:
                                    val2 = int(val)
                                    fields[key] = val+"i"
                                except Exception as e:
                                    try:
                                        val2 = float(val)
                                        fields[key] = val2
                                    except Exception as e:
                                        tags[key] = val

                            elif type(val) in [int,long]:
                                fields[key] = str(val) + "i"
                            else:
                                fields[key] = val

                    l_timestamp = int(metricas["timestamp"] if "timestamp" in metricas else time.mktime(now.timetuple()))
                    if base.Settings.PRECISION == "ms":
                        l_timestamp = l_timestamp * 1000
                    elif base.Settings.PRECISION == "ns":
                        l_timestamp = l_timestamp * 1000 * 1000
                    elif base.Settings.PRECISION == "us":
                        l_timestamp = l_timestamp * 1000 * 1000 * 1000

                    l_date = now.strftime("%Y-%m-%d")
                    l_time = now.strftime("%H:%M:%S")
                    tagsstr = ""
                    tags['version'] = version.strip()
                    if tags:
                        str_tags = []
                        for key, val in tags.items():
                            if val is None:
                                continue
                            normalized_val = val.replace("'", "").replace('"', "").replace("\\", "\\\\").replace("=","\\=").replace(" ", "\\ ")
                            if normalized_val:
                                str_tags.append(get_tag_compat(self.instance.technology, modulo, key) + "=" + normalized_val)
                        tagsstr = "," + ",".join(str_tags)
                    metricssstr2 = ""
                    if fields:
                        str_fields = []
                        for key, val in fields.items():
                            if str(val):
                                str_fields.append(get_field_compat(self.instance.technology, modulo, key) + "=" + str(val))
                        metricssstr2 = ",".join(str_fields)
                    _formatted_metrics.append(self.formatter.FORMAT.format(
                                                            timestamp=l_timestamp,
                                                            host=host.upper(),
                                                            date=l_date,
                                                            time=l_time,
                                                            measurement=get_measurement_compat(self.instance.technology, modulo),
                                                            tags=tagsstr,
                                                            metrics=metricssstr2))
        return _formatted_metrics

    def write(self,host,modulo,metricasobj):
        LOG.error("Not implemented.")
        raise NotImplementedError

