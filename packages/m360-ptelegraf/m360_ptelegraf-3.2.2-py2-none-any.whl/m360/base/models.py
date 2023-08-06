import collections
import datetime
import time
import re
import hashlib
from m360.base.settings import Settings

dxcmms_data_format = "{timestamp} {host} {date} {time} {tech} \"{version}\" {instance} {metrics}"

# Declaring namedtuple()
MTuple = collections.namedtuple('MTuple', ['key', 'value'])


class Timeseries(object):
    def __init__(self):
        self._internal = {}
        self._global_tags = {}

    def add_global_tag(self,key,value):
        self._global_tags[key]=value

    @property
    def global_tags(self):
        return self._global_tags

    def add_serie(self,metric):
        if metric.serie_id in self._internal:
            for field in metric.fields:
                self._internal[metric.serie_id].add_field(key=field.key,val=field.value)
        else:
            self._internal[metric.serie_id] = metric

    def get_series(self):
        return [value for id,value in self._internal.items()]


class Metrics(object):

    def __init__(self, measurement, timestamp=0, tags=None, fields=None,exclude_tags=None):
        if tags is None:
            tags = []
        if fields is None:
            fields = []
        if timestamp:
            self._timestamp = int(timestamp)
        else:
            self._timestamp = int(time.time())

        self._measurement = measurement.strip().replace(" ","")
        self._tags = Metrics.dict_to_MTuples(tags,exclude_tags)
        self._fields = []
        for f in Metrics.dict_to_MTuples(fields):
                self.add_field(f.key, f.value)

        _tag_string = ",".join([tuple.key+"="+tuple.value for tuple in self._tags])
        _str = self._measurement + str(self._timestamp) + _tag_string
        self._serie_id = hashlib.md5(_str.encode()).hexdigest()

        assert len(self._fields) > 0
        assert self._timestamp > 0


    @staticmethod
    def dict_to_MTuples(a,exclude_keys=None):
        if exclude_keys is None:
            exclude_keys = []

        if type(a) is list:
            return a
        ret = []
        for name, value in a.items():
            if name not in exclude_keys:
                ret.append(MTuple(name,value))
        return sorted(ret, key=lambda x: x.key, reverse=True)

    @property
    def serie_id(self):
        return self._serie_id

    @property
    def all(self):
        return self._tags + self._fields

    @property
    def tags(self):
        return self._tags

    @property
    def fields(self):
        return self._fields

    def add_field(self,key="",val=""):
        if key:
            if key=="timestamp":
                try:
                    self._timestamp = int(val)
                except Exception as e:
                    pass
            else:
                try:
                    if val == 0 or val == "0":
                        self._fields.append(MTuple(key,0))
                    else:
                        self._fields.append(MTuple(key, float(val)))
                except Exception as e:
                    if val:
                        self._tags.append(MTuple(key,val))


    @property
    def timestamp(self):
        return self._timestamp

    @property
    def measurement(self):
        return self._measurement

    #FORMATOS
    #'%{metricaid} %{metricavalue} %{time}
    def graphite(self,**kwargs):
        ret = []
        template = "{"+kwargs['template'].replace(".","}.{")+"}"

        l_timestamp = str(self._timestamp)
        l_global_tags = []
        if 'global_tags' in kwargs and kwargs['global_tags'] is not None:
            l_global_tags_str = ".".join(re.sub(r"[\\\s\./]","-",val) for key,val in kwargs['global_tags'].iteritems())
            if l_global_tags_str:
                l_global_tags = [l_global_tags_str]

        host = ""
        if 'agent' in kwargs:
            host = kwargs['agent'].hostname

        l_metric_tags = []
        l_metric_tags_str = ".".join(re.sub(r'[\\\s\./]',"-",item.value) for item in self._tags)
        if l_metric_tags_str:
            l_metric_tags = [l_metric_tags_str]
        for field in self._fields:
            l_metricid_base = template.format(host=host,
                                              tags=".".join(l_global_tags + l_metric_tags),
                                              measurement= self.measurement,
                                              field= field.key)
            ret.append(l_metricid_base.replace("..",".")+" "+str(field.value)+" "+l_timestamp+"\n")

        return "".join(ret)

    def json(self,**kwargs):
        l_global_tags = []
        if 'global_tags' in kwargs and kwargs['global_tags'] is not None:
            l_global_tags = [",".join("'" + key + "': '" + val + "'" for key,val in kwargs['global_tags'].iteritems())]
        l_metric_tags = [",".join("'"+item.key+"': '"+item.value+"'" for item in self._tags)]

        return "{'measurement': '"+self._measurement+"'," + \
               "'tags': ["+",".join(l_global_tags+l_metric_tags)+"]," + \
               "'fields': ["+",".join("'"+item.key+"': "+item.value for item in self._fields)+"]," + \
               "'timestamp': "+str(self._timestamp)+"}"

    def dxcmms(self,**kwargs):
        l_global_tags = []
        if 'global_tags' in kwargs and kwargs['global_tags'] is not None:
            l_global_tags = ["%s_%s_%s%s:\"%s\"" % (Settings.TECHABRV[kwargs['instance'].technology],
                                    kwargs['modulo'].replace("_", "."),
                                    key if key.find(":") < 0 else key.split(":")[0],
                                    "V1" if key.find(":") < 0 else key.split(":")[1],
                                    value.replace("\\", "\\\\").replace("\"", "\\\"")) for key,value in kwargs['global_tags'].items()]

        metrics_str = ' '.join(l_global_tags +
                               ["%s_%s_%s%s:\"%s\"" % (Settings.TECHABRV[kwargs['instance'].technology],
                                                  kwargs['modulo'].replace("_","."),
                                                  mtuple.key if mtuple.key.find(":")<0 else mtuple.key.split(":")[0],
                                                  "V1" if mtuple.key.find(":")<0 else mtuple.key.split(":")[1],
                                                  mtuple.value.replace("\\","\\\\").replace("\"", "\\\"")) for mtuple in self.tags] +
                               ["%s_%s_%s%s:%s" % (Settings.TECHABRV[kwargs['instance'].technology],
                                                  kwargs['modulo'].replace("_","."),
                                                  mtuple.key if mtuple.key.find(":")<0 else mtuple.key.split(":")[0],
                                                  "V1" if mtuple.key.find(":")<0 else mtuple.key.split(":")[1],
                                                  mtuple.value) for mtuple in self.fields]
                               ).strip()
        now = datetime.datetime.now()
        l_date = now.strftime("%Y-%m-%d")
        l_time = now.strftime("%H:%M:%S")
        l_kwargs = {"metrics": metrics_str,
                    "timestamp": self.timestamp,
                    "host": kwargs['host'].upper(),
                    "date": l_date,
                    "time": l_time,
                    "tech": kwargs['instance'].technology,
                    "version": kwargs['instance'].version,
                    "instance": kwargs['instance'].name
                    }

        return dxcmms_data_format.format(**l_kwargs)

    def influx(self, **kwargs):
        l_measurement = self._measurement
        l_tags = ""
        if 'global_tags' in kwargs and kwargs['global_tags'] is not None:
            l_tags += "," + ",".join([key + "=" + str(val).replace("'", "").replace('"', "").replace(" ","\\ ") for key,val in kwargs['global_tags'].items()])
        if self._tags:
            l_tags += "," + ",".join([item.key+"="+str(item.value).replace("'", "").replace('"', "").replace(" ","\\ ") for item in self._tags])
        l_fields = " " + ",".join([item.key+"="+str(item.value) for item in self._fields])
        l_timestamp = " " + str(self._timestamp)

        return l_measurement + l_tags + l_fields + l_timestamp

    @staticmethod
    def influx_format(raw_line):
        l_parts = raw_line.split(",")
        l_tags = {}
        l_fields = {}
        return Metrics(measurement=l_parts[0],tags=l_tags,fields=l_fields,timestamp=int())

    @staticmethod
    def raw_data_format(lines,format_func=influx_format):
        array_metrics = []
        for l in lines:
            array_metrics.append(format_func(l))
        return array_metrics
