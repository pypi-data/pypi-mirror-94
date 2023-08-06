#Autoconfigured 29-10-2018 23:47
import m360.base.settings as base
import os


class Settings (base.Settings):
    MONITOR_TECHNOLOGY = os.path.basename(os.path.dirname(__file__))
    SLEEP_BEFORE_CPU=5
    INTERVAL_CPU=1.0