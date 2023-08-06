import time
from m360.agents.oraclecloud.settings import Settings
from oci.monitoring import MonitoringClient
from oci.config import from_file
from oci.identity import IdentityClient
from oci.monitoring.models import SummarizeMetricsDataDetails
from datetime import datetime, timedelta
from dateutil import tz
from oci.exceptions import ServiceError
from m360.base.models import Metrics, MTuple, Timeseries


class Manager(object):

    def __init__(self,file_location='oci.conf'):
        self._conf = from_file(file_location=file_location)
        self._identity = IdentityClient(self._conf)
        self._metricsClient = MonitoringClient(self._conf)

    def get_autonomous(self,compartiment_id):
        _data = Timeseries()

        _metrics = Settings._namespaces[Settings.AUTONOMOUS]
        metricObj = None
        for _metric in _metrics:
            _response = None
            try:
                _response = self.query(compartiment_id, Settings.AUTONOMOUS, _metric + "[5m].last()")
            except ServiceError as e:
                ##retry after X msegs
                time.sleep(1)
                try:
                    _response = self.query(compartiment_id, Settings.AUTONOMOUS, _metric + "[5m].last()")
                except Exception as e:
                    pass
            finally:
                if _response and _response.data:
                    for i in _response.data:
                        for datapoint in i.aggregated_datapoints:
                            _timestamp = datapoint.timestamp
                            HERE=tz.tzlocal()
                            UTC=tz.gettz('UTC')
                            _timestamp = (_timestamp.replace(tzinfo=UTC) - datetime(1970, 1, 1, tzinfo=UTC)).total_seconds()
                            _timestamp = int(_timestamp * 1000 * 1000 * 1000)
                            metricObj = Metrics(Settings.AUTONOMOUS,
                                                _timestamp,
                                                i.dimensions,
                                                [MTuple(i.name,str(datapoint.value))],
                                                ["displayName","resourceId"])
                            _data.add_serie(metricObj)
        return _data

    def query(self,compartment_id,namespace,query,deltatime=5):
        if not compartment_id or not namespace or not query:
            return {}
        now = datetime.utcnow()
        start =  now - timedelta(minutes=deltatime)
        end = now

        _metrics_details = {
            'query': query,
            'namespace': namespace,
            'resolution': str(deltatime)+'m',
            'start_time': start,
            'end_time': end
        }
        metrics_details = SummarizeMetricsDataDetails(**_metrics_details)
        data = self._metricsClient.summarize_metrics_data(compartment_id, metrics_details)
        return data
