from m360.base.output import OutputBase


class Output(OutputBase):
    def write(self,host,modulo,metricasobj):
        _formatted_metrics = self.get_formatted_metrics(host, modulo, metricasobj)
        if _formatted_metrics:
            with open(self.conf['filename'], 'a') as f:
                for line in _formatted_metrics:
                    f.write(line + "\n")
