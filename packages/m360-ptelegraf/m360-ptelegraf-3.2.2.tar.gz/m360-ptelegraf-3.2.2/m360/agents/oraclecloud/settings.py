#Autoconfigured 29-10-2018 23:47
import m360.base.settings as base
import os


class Settings(base.Settings):
    MONITOR_TECHNOLOGY = os.path.basename(os.path.dirname(__file__))
    HEALTH = "oci_healthchecks"

    _namespaces = {
        base.Settings.AUTONOMOUS: ["ApplyLag", "BlockChanges", "ConnectionLatency", "CpuTime", "CpuUtilization",
                                    "CurrentLogons", "DBTime", "ExecuteCount", "FailedConnections", "FailedLogons",
                                    "IOPS", "IOThroughput", "LogicalBlocksRead", "OCPUsAllocated", "ParsesByType",
                                    "ParseCount", "QueryLatency", "QueuedStatements", "RedoSize",
                                    "RunningStatements", "Sessions", "StorageAllocated",
                                    "StorageAllocatedByTablespace", "StorageUsed", "StorageUsedByTablespace",
                                    "StorageUtilization", "StorageUtilizationByTablespace", "TransactionsByStatus",
                                    "TransactionCount", "TransportLag", "UserCalls", "WaitTime"],
        "oci_healthchecks": []

    }
