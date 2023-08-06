MEASUREMENTS={
    "unix":{
        "health":"unix_health"
    }
}

TAGS={
    "unix":{
        "mountpoint":"path"
    }
}

FIELDS={
    "unix":{
        "system": {
            "runqueue1":"load1",
            "runqueue15":"load15",
            "runqueue5": "load5"
        },
        "cpu":{
            "user": "usage_user",
            "system": "usage_system",
            "idle": "usage_idle",
            "nice": "usage_nice",
            "iowait": "usage_iowait",
            "irq": "usage_irq",
            "softirq": "usage_softirq",
            "steal": "usage_steal",
            "guest": "usage_guest",
            "guest_nice": "usage_guest"
        },
        "mem":{
            "percent": "used_percent"
        },
        "swap":{
            "sin":"in",
            "sout": "out",
            "percent": "used_percent"
        },
        "disk":{
            "percent":"used_percent",
            "size":"total"
        },
        "net":{
            "errin":"err_in",
            "errout":"err_out",
            "dropin":"drop_in",
            "dropout":"drop_out"
        }
    }
}

def get_measurement_compat(tech,module):
    if tech in MEASUREMENTS:
        if isinstance(MEASUREMENTS[tech], basestring):
            return MEASUREMENTS[tech]
        elif module in MEASUREMENTS[tech]:
            return MEASUREMENTS[tech][module]
        elif tech == "unix":
            return module
        else:
            return tech + "_" + module
    else:
        return tech+"_"+module

def get_tag_compat(tech,module,key):
    if tech in TAGS:
        if module in TAGS[tech] and key in TAGS[tech][module]:
            return TAGS[tech][module][key]
        elif key in TAGS[tech]:
            return TAGS[tech][key]
    return key

def get_field_compat(tech,module,key):
    if tech in FIELDS:
        if module in FIELDS[tech] and key in FIELDS[tech][module]:
            return FIELDS[tech][module][key]
        elif key in FIELDS[tech]:
            return FIELDS[tech][key]
    return key
