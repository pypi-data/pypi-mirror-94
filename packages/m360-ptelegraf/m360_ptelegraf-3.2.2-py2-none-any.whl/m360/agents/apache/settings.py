#Autoconfigured 12-11-2018 12:31
import m360.base.settings as base
import os


class Settings (base.Settings):
    MONITOR_TECHNOLOGY = os.path.basename(os.path.dirname(__file__))
    APACHE_CONFPATH = "/usr/local/apache24"
