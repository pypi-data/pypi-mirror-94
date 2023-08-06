import sys

from m360.base.output import OutputBase


class Output(OutputBase):
    def write(self,host,modulo,metricasobj):
        _formatted_metrics = self.get_formatted_metrics(host, modulo, metricasobj)
        for line in _formatted_metrics:
            sys.stdout.write(line+"\n")
        sys.stdout.flush()
