class Formatter(object):
    FORMAT = "{measurement}{tags} {metrics} {timestamp}"

    def __init__(self):
        pass

    def format(self,data,**kwargs):
        format_arr = []
        for metric in data.get_series():
            format_arr.append(metric.dxcmms(global_tags=data.global_tags,**kwargs))
        return format_arr

