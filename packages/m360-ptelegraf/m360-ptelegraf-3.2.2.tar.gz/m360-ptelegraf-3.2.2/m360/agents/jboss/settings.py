#Autoconfigured 10-09-2018 11:47
import m360.base.settings as base
import os


class Settings (base.Settings):
    MONITOR_TECHNOLOGY = os.path.basename(os.path.dirname(__file__))
