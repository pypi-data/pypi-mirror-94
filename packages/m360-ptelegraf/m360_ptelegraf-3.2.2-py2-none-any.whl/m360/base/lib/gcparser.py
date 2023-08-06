import re
from logging import getLogger

LOG = getLogger('m360.base.lib')

# Error type for parser.
class ParseError(Exception):
    pass

"""
This is a parser of GC log of Sun HotSpot JVM Version 6.

Required JVM option: -Xloggc=${GC_LOG_FILE} -XX:+PrintGCDetails

Usage:
   java -Xloggc=${GC_LOG_FILE} -XX:+PrintGCDetails ${ANY_OTHER_OPTIONS}
   this.py < ${GC_LOG_FILE} | grep -v ^### | ${YOUR_ANALYZER}

You can get all data as a python dictionary structure
in your analyer as follows:

import sys
import json

list = []
for line in sys.stdin:
    line.rstrip()
    list.append(dict(json.loads(line)))

"""

################################################################################
# Parser generator from regular expression.
################################################################################

"""
Generate a parser from regex pattern and modifier.

Parser try to match input text by the pattern.
If matched, call data_modifier with list of matched strings.
The modifier add/update tag_str of the dictionary.

regexStr :: String
dataModifier :: (a, [String]) -> a | None
return :: (String, a) -> (String, a)
a :: ANY

dataModifier must not throw exceptions.
When some errors occur inside dataModifier, a must be not modified.

"""

def newP(regexStr, dataModifier,optional=False):
    l_regex="(^%s)?" if optional else "(^%s)"
    p = re.compile(l_regex % regexStr)

    def parse_(line, data):
        m = p.match(line)
        if m:
            if line=='' and optional:
                return ("", data)
            l_grups=m.groups()
            if dataModifier is not None:
                data = dataModifier(data, m.groups()[1:])
            return (line[len(m.group(1)):], data)
        else:
            msg = "Parse failed: pattern \"%s\" for \"%s\"" % (regexStr, line)
            raise ParseError(msg)

    return parse_


################################################################################
# Utilities.
################################################################################

"""
Just modify data during parse.

dataModifier :: (a, [String]) -> a
return :: (String, a) -> (String, a)
a :: ANY

"""

def appP(dataModifier):
    def modify_(line, data):
        if dataModifier is not None:
            data = dataModifier(data)
        return (line, data)

    return modify_


# [String] -> String
def toString(strL):
    ret = "[%s" % strL[0]
    for str in strL[1:]:
        ret += ", %s" % str
    ret += "]"
    return ret


################################################################################
# Parser combinators.
################################################################################

"""
Parser combinator AND.

parsers :: [Parser]
return :: Parser

"""

def andP(parsers):
    def parseAnd_(text, data):
        text0 = text
        data0 = data
        for parser in parsers:
            (text1, data1) = parser(text0, data0)
            text0 = text1
            data0 = data1
        return (text0, data0)

    return parseAnd_


"""
Parser combinator OR.

parsers :: [Parser]
return :: Parser

"""

def orP(parsers):
    def parseOr_(text, data):
        msgL = []
        for parser in parsers:
            try:
                (ret_text, ret_data) = parser(text, data)
                return (ret_text, ret_data)
            except ParseError as msg:
                msgL.append(msg)
        msgs = toString(msgL)
        raise ParseError(msgs)

    return parseOr_


"""
Parser combinator MANY.
parsers :: [Parser]
return :: Parser

"""

def manyP(parser):
    def parseMany_(text, data):
        text0 = text
        data0 = data
        text1 = text
        data1 = data
        try:
            while True:
                (text1, data1) = parser(text0, data0)
                text0 = text1
                data0 = data1
        except ParseError as msg:
            if __debug__:
                LOG.debug("Error parsing: %s",msg,extra={"monitor":"NA","modulo":"Gc"})
        return (text1, data1)

    return parseMany_


################################################################################
# Utilities.
################################################################################

"""
A modifier for dictionary data.

tagStr :: String
dataConstructor :: [String] -> ANY
return :: (Dictionary, [String]) -> Dictionary

"""

def mkDictModifier(tagStr, dataConstructor,postTags=None):
    def modifyNothing_(dictData, matchStringL):
        return dictData

    if tagStr is None or dataConstructor is None:
        return modifyNothing_

    def modifyDict_(dictData, matchStringL):
        if matchStringL is None:
            return dictData
        l_data = dataConstructor(matchStringL)
        if postTags and len(postTags)==len(l_data):
            for i in range(len(postTags)):
                dictData[tagStr+"_"+postTags[i]]=l_data[i]
        else:
            dictData[tagStr] = dataConstructor(matchStringL)
        return dictData

    return modifyDict_


"""
Behave like newP but that parses anything, just modify dictionary.

key :: String
value :: ANY
return :: (String, Dictionary) -> (String, Dictionary)

"""
def factor(unit):
    l_factor = 1
    if unit == "K":
        l_factor = 1024
    elif unit == "M":
        l_factor = 1024 * 1024
    elif unit == "G":
        l_factor = 1024 * 1024
    return l_factor


def mkTagger(key, value):
    def tagger_(line, dictData):
        dictData[key] = value
        return (line, dictData)

    return tagger_


# match_strL :: [String] # length must be 1.
# return :: Float
def get_float(match_strL):
    assert len(match_strL) == 1
    return float(match_strL[0].replace(',','.'))


# match_strL :: [String] # length must be 6.
# return :: [Int] # length is 3.
def get_int3_units(match_strL):
    assert len(match_strL) == 6
    return [int(match_strL[0].replace(',','.'))*factor(match_strL[1]),
            int(match_strL[2].replace(',','.'))*factor(match_strL[3]),
            int(match_strL[4].replace(',','.'))*factor(match_strL[5])]

# match_strL :: [String] # length must be 3.
# return :: [Int] # length is 3.
def get_int3(match_strL):
    assert len(match_strL) == 3
    return [int(match_strL[0].replace(',','.')),
            int(match_strL[1].replace(',','.')),
            int(match_strL[2].replace(',','.'))]

# match_strL :: [String] # length must be 3
# return :: [FLoat] # length is 3.
def get_float3(match_strL):
    assert len(match_strL) == 3
    return [float(match_strL[0].replace(',','.')), float(match_strL[1].replace(',','.')), float(match_strL[2].replace(',','.'))]

# match_strL :: [String] # length must be 4.
# return :: [Int] # length is 4.
def get_float2_units(match_strL):
    assert len(match_strL) == 4
    return [float(match_strL[0].replace(',','.'))*factor(match_strL[1]),
            float(match_strL[2].replace(',','.'))*factor(match_strL[3])]

# match_strL :: [String] # length must be 6
# return :: [FLoat] # length is 3.
def get_float3_units(match_strL):
    assert len(match_strL) == 6
    return [float(match_strL[0].replace(',','.'))*factor(match_strL[1]),
            float(match_strL[2].replace(',','.'))*factor(match_strL[3]),
            float(match_strL[4].replace(',','.'))*factor(match_strL[5])]

# match_strL :: [String] # length must be 8.
# return :: [Int] # length is 4.
def get_float4_units(match_strL):
    assert len(match_strL) == 8
    return [float(match_strL[0].replace(',','.'))*factor(match_strL[1]),
            float(match_strL[2].replace(',','.'))*factor(match_strL[3]),
            float(match_strL[4].replace(',','.'))*factor(match_strL[5]),
            float(match_strL[6].replace(',','.'))*factor(match_strL[7])]

# match_strL :: [String]
# return :: True
def get_true(match_strL):
    return True


################################################################################
# Regexp aliases.
################################################################################

regexp_float = r"(\d+[\.,]?\d*)"
regexp_float_colon = regexp_float + r":\s+"
regexp_unit = r"(G|M|K|B)"
regexp_heap_info = r"(\d+)K->(\d+)K\((\d+)K\)"
#192.0M(2400.0M)->0.0B(2352.0M)
regexp_heap_info_units = regexp_float+regexp_unit+r"->"+regexp_float+regexp_unit+"\("+regexp_float+regexp_unit+"\)"
regexp_heap_info_g1 = regexp_float+regexp_unit+r"\("+regexp_float+regexp_unit+r"\)->"+regexp_float+regexp_unit+r"\("+regexp_float+regexp_unit+r"\)"
regexp_float_secs = regexp_float + r"\s*secs\s+"
regexp_basic_string = r"([0-9a-zA-Z_-]+)"
#[Times: user=0.11 sys=0.00, real=0.13 secs]
regexp_times_float = r"\[Times:\s+user="+regexp_float+"\s+sys="+regexp_float+",\s+real="+regexp_float+"\s+secs\]"
#192.0M->2352.0M
regexp_heap_info2_units = regexp_float+regexp_unit+"->"+regexp_float+regexp_unit

################################################################################
# Parsers for gc log entries.
################################################################################

parseParNew = andP([
    mkTagger("type", "ParNew"),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    newP(r"\[GC\s+", None),
    newP(regexp_float_colon, None),
    newP(r"\[ParNew:\s+", None),
    newP(regexp_heap_info + r",\s+", mkDictModifier("heap_new", get_int3)),
    newP(regexp_float + r"\s*secs\]\s*", None),
    newP(regexp_heap_info, mkDictModifier("heap_all", get_int3)),
    newP(r"\s*(?:icms_dc=\d+\s*)?", None),
    newP(r",\s*", None),
    newP(regexp_float + r"\s*secs\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseInitialMark = andP([
    mkTagger("type", "CMS-initial-mark"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r".*CMS-initial-mark:.*$", None),
    ])

parseMarkStart = andP([
    mkTagger("type", "CMS-concurrent-mark-start"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r".*CMS-concurrent-mark-start.*$", None),
    ])

parseMark = andP([
    mkTagger("type", "CMS-concurrent-mark"),
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)),
    newP(r"\[CMS-concurrent-mark:\s+", None),
    newP(regexp_float + r"/", None),
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parsePrecleanStart = andP([
    mkTagger("type", "CMS-concurrent-preclean-start"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r".*CMS-concurrent-preclean-start.*$", None),
    ])

parsePreclean = andP([
    mkTagger("type", "CMS-concurrent-preclean"),
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)),
    newP(r"\[CMS-concurrent-preclean:\s+", None),
    newP(regexp_float + r"/", None),
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseAbortablePrecleanStart = andP([
    mkTagger("type", "CMS-concurrent-abortable-preclean-start"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r".*CMS-concurrent-abortable-preclean-start.*$", None),
    ])

parseAbortablePreclean = andP([
    mkTagger("type", "CMS-concurrent-abortable-preclean"),
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)),
    newP(r"\[CMS-concurrent-abortable-preclean:\s+", None),
    newP(regexp_float + r"/", None),
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseAbortablePrecleanFullGC0 = andP([
    mkTagger("type", "CMS-concurrent-abortable-preclean-fullgc0"),
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)),
    orP([
        newP(r"\[Full GC\s*\(System\)\s*" + regexp_float + r":\s+", mkDictModifier("system", get_true)),
        newP(r"\[Full GC\s*" + regexp_float + r":\s+", None),
        ]),
    newP(r"\[CMS" + regexp_float + r":\s+", None),
    newP(r"\[CMS-concurrent-abortable-preclean:\s+", None),
    newP(regexp_float + r"/", None),
    newP(regexp_float + r"\s+secs\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseAbortablePrecleanFullGC1 = andP([
    mkTagger("type", "CMS-concurrent-abortable-preclean-fullgc1"),
    newP(r"\s*\(concurrent mode (failure|interrupted)\):\s+", None),
    newP(regexp_heap_info + r",\s+", mkDictModifier("heap_1", get_int3)),
    newP(regexp_float + r"\s+secs\s*\]\s+", None),
    newP(regexp_heap_info + r",\s+", mkDictModifier("heap_2", get_int3)),
    newP(r"\[CMS Perm\s+:\s+", None),
    newP(regexp_heap_info + r"\],\s+", mkDictModifier("perm", get_int3)),
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseAbortablePrecleanFailureTime = andP([
    mkTagger("type", "CMS-concurrent-abortable-preclean-failure-time"),
    newP(r"\s*CMS:\s*abort preclean due to time\s*", None),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    newP(r"\[CMS-concurrent-abortable-preclean:\s*", None),
    newP(regexp_float + r"/", None),
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseRemark = andP([
    mkTagger("type", "CMS-remark"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r"\[GC\[YG occupancy.+CMS-remark:\s+\d+K\(\d+K\)\]\s*", None),
    newP(r"\d+K\(\d+K\),\s*", None),
    newP(regexp_float + r"\s*secs\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseSweepStart = andP([
    mkTagger("type", "CMS-concurrent-sweep-start"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r"\[CMS-concurrent-sweep-start\]$", None),
    ])

parseSweep = andP([
    mkTagger("type", "CMS-concurrent-sweep"),
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)),
    newP(r"\[CMS-concurrent-sweep:\s+", None),
    newP(regexp_float + r"/", None),
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseResetStart = andP([
    mkTagger("type", "CMS-concurrent-reset-start"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP("\[CMS-concurrent-reset-start\]$", None),
    ])

parseReset = andP([
    mkTagger("type", "CMS-concurrent-reset"),
    newP(regexp_float + r":\s+", mkDictModifier("timestamp", get_float)),
    newP(r"\[CMS-concurrent-reset:\s+", None),
    newP(regexp_float + r"/", None),
    newP(regexp_float + r"\s+secs\]\s+", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

parseFullGC = andP([
    mkTagger("type", "FullGC"),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    orP([
        newP(r"\[Full GC\s*\(System\)\s*", mkDictModifier("system", get_true)),
        newP(r"\[Full GC\s*", None),
        ]),
    newP(regexp_float_colon, None),
    newP(r"\[CMS:\s+", None),
    newP(regexp_heap_info + r",\s+", mkDictModifier("heap_cms", get_int3)),
    newP(regexp_float + r"\s*secs\]\s*", None),
    newP(regexp_heap_info, mkDictModifier("heap_all", get_int3)),
    newP(r"\s*,\s*\[CMS Perm\s*:\s*", None),
    newP(regexp_heap_info, mkDictModifier("perm", get_int3)),
    newP(r"\]\s*(?:icms_dc=\d+\s*)?", None),
    newP(r",\s*", None),
    newP(regexp_float + r"\s*secs\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

# This is for -XX:+UseParallelGC
parseParallelGC = andP([
    mkTagger("type", "ParallelGC"),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    newP(r"\[GC\s+\[PSYoungGen:\s*", None),
    newP(regexp_heap_info + r"\s*\]\s*", mkDictModifier("heap_new", get_int3)),
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_all", get_int3)),
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

# This is for -XX:+UseParallelGC
parseParallelFullGC = andP([
    mkTagger("type", "ParallelFullGC"),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    orP([
        newP(r"\[Full GC\s*\(System\)\s*\[PSYoungGen:\s*", mkDictModifier("system", get_true)),
        newP(r"\[Full GC\s*\[PSYoungGen:\s*", None),
        ]),
    newP(regexp_heap_info + r"\s*\]\s*", mkDictModifier("heap_new", get_int3)),
    newP(r"\[PSOldGen:\s*", None),
    newP(regexp_heap_info + r"\s*\]\s*", mkDictModifier("heap_old", get_int3)),
    newP(regexp_heap_info + r"\s*", mkDictModifier("heap_all", get_int3)),
    newP(r"\[PSPermGen:\s*", None),
    newP(regexp_heap_info + r"\s*\]\s*,\s*", mkDictModifier("perm", get_int3)),
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

# This is for -XX:+UseSerialGC
parseSerialGC = andP([
    mkTagger("type", "SerialGC"),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    newP(r"\[GC\s+", None),
    newP(regexp_float_colon + r"\[DefNew:\s*", None),
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_new", get_int3)),
    newP(regexp_float + r"\s*secs\s*\]\s*", None),
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_all", get_int3)),
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

# This is for -XX:+UseSerialGC
parseSerialFullGC = andP([
    mkTagger("type", "SerialFullGC"),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    newP(r"\[Full GC\s+", None),
    newP(regexp_float_colon + r"\s*", None),
    newP(r"\[Tenured:\s*", None),
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_old", get_int3)),
    newP(regexp_float + r"\s*secs\]\s*", None),
    newP(regexp_heap_info + r"\s*,\s*", mkDictModifier("heap_all", get_int3)),
    newP(r"\[Perm\s*:\s*", None),
    newP(regexp_heap_info + r"\s*\]\s*,\s*", mkDictModifier("perm", get_int3)),
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("response", get_float)),
    newP(r"\[Times:.*\]$", None),
    ])

# This is for DEFAULT GC mode. No other option defined
parseDefaultMinorGC = andP([
    mkTagger("type", "DefaultGC"),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    newP(r"\[GC\s*(\([^\)]*\))?\s*\[PSYoungGen:\s*",None),
    newP(regexp_heap_info + r"\s*\]\s*", mkDictModifier("heap_young", get_int3,["used_before","used_after","total_after"])),
    newP(regexp_heap_info + r",\s*", mkDictModifier("heap_all", get_int3,["used_before","used_after","total_after"])),
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("duration", get_float)),
    newP(regexp_times_float+r"$", mkDictModifier("duration", get_float3,["user","sys","real"]),optional=True),
    ])

parseDefaultFullGC = andP([
    mkTagger("type", "DefaultFullGC"),
    newP(regexp_float_colon, mkDictModifier("timestamp", get_float)),
    newP(r"\[Full GC\s*(\([^\)]*\))?\s*\[PSYoungGen:\s*",None),
    newP(regexp_heap_info + r"\s*\]\s*", mkDictModifier("heap_young", get_int3,["used_before","used_after","total_after"])),
    newP(regexp_heap_info + r",\s*", mkDictModifier("heap_all", get_int3,["used_before","used_after","total_after"])),
    newP(regexp_float + r"\s*secs\s*\]\s*", mkDictModifier("duration", get_float)),
    newP(regexp_times_float+r"$", mkDictModifier("duration", get_float3,["user","sys","real"]),optional=True),
    ])

parseDefaultGC = orP([
        parseDefaultMinorGC,
        parseDefaultFullGC,
    ])

# -XX:+UseG1GC
parseRemarkGC1 = andP([
    mkTagger("type", "gc1-remark"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP("\[GC remark\s*", None),
    newP(regexp_float + r":\s*",None),
    newP("\[Finalize Marking,\s+"+regexp_float+"\s+secs\]\s*", mkDictModifier("duration_finalize", get_float)),
    newP(regexp_float + r":\s*",None),
    newP("\[GC ref-proc,\s+"+regexp_float+"\s+secs\]\s*", mkDictModifier("duration_ref_proc", get_float)),
    newP(regexp_float + r":\s*",None),
    newP("\[Unloading,\s+"+regexp_float+"\s+secs\]\s*", mkDictModifier("duration_unloading", get_float)),
    newP(",\s+"+regexp_float+"\s+secs\]\s*", mkDictModifier("duration", get_float)),
    ])

parsePause = andP([
    mkTagger("type", "pause"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP("\[GC\s+pause\s+[^,]*,\s*"+regexp_float+"\s+secs\]\s*", mkDictModifier("duration", get_float)),
    ])

parseCleanup = andP([
    mkTagger("type", "cleanup"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP("\[GC\s+cleanup\s+", None),
    newP(regexp_heap_info_units, mkDictModifier("heap_all", get_float3_units,["used_before","used_after","total_after"])),
    newP(",\s*"+regexp_float+"\s+secs\]\s*", mkDictModifier("duration", get_float)),
    ])

parseCleanupStart = andP([
    mkTagger("type", "cleanup-start"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP("\[GC\s+concurrent-cleanup-start\]\s*", None),
    ])

parseCleanupEnd = andP([
    mkTagger("type", "cleanup-end"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP("\[GC\s+concurrent-cleanup-end\s*,", None),
    newP("\s*" + regexp_float + "\s+secs\]\s*", mkDictModifier("duration", get_float)),
])

parseMarkStartGC1 = andP([
    mkTagger("type", "mark-start"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r".*concurrent-mark-start.*$", None),
    ])

parseMarkEndGC1 = andP([
    mkTagger("type", "mark-end"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r"\[GC\s+concurrent-mark-end\s*,", None),
    newP("\s*" + regexp_float + "\s+secs\]\s*", mkDictModifier("duration", get_float)),
    ])

parseScanStart = andP([
    mkTagger("type", "scan-start"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r".*scan-start.*$", None),
    ])

parseScanEnd = andP([
    mkTagger("type", "scan-end"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP(r"\[GC\s+[^,]*scan-end\s*,", None),
    newP("\s*" + regexp_float + "\s+secs\]\s*", mkDictModifier("duration", get_float)),
    ])

parseEden = andP([
        mkTagger("type", "eden-heap"),
        newP(r"\s*\[Eden:\s*" + regexp_heap_info_g1 + "\s+", mkDictModifier("heap_eden", get_float4_units,
                                                                            ["used_before", "total_before",
                                                                             "used_after", "total_after"])),
        newP(r"\s*Survivors:\s*" + regexp_heap_info2_units + "\s+",
             mkDictModifier("heap_survivor", get_float2_units, ["used_before", "used_after"])),
        newP(r"\s*Heap:\s*" + regexp_heap_info_g1 + "\s*\]\s*", mkDictModifier("heap_all", get_float4_units,
                                                                                ["used_before", "total_before",
                                                                                 "used_after", "total_after"])),
        newP(r",\s*\[\s*Metaspace:\s*" + regexp_heap_info_units + "\s*\]\s*", mkDictModifier("heap_metaspace", get_float3_units,
                                                                                ["used_before", "used_after", "total_after"])
                                                                            ,optional=True),
])

parseTimes = andP([
    mkTagger("type", "times"),
    newP(r"\s*"+regexp_times_float+"\s*", mkDictModifier("duration", get_float3,["user","sys","real"])),
    ])

parseFullGC1 = andP([
    mkTagger("type", "fullgc1"),
    newP(regexp_float + r":\s*", mkDictModifier("timestamp", get_float)),
    newP("\[Full\s+GC\s+\(.*\)\s+"+regexp_heap_info_units,mkDictModifier("heap_all", get_float3_units,['used_before','used_after','total_after'])),
    newP(",\s*"+regexp_float+"\s+secs\]\s*", mkDictModifier("duration", get_float)),
    ])

parseG1GC = orP([
    parseCleanup,
    parseCleanupStart,
    parseCleanupEnd,
    parseMarkStartGC1,
    parseMarkEndGC1,
    parseScanStart,
    parseScanEnd,
    parseRemarkGC1,
    parsePause,
    parseFullGC1,
])


"""
Java GC Log parser.
This supports almost kinds of GC provided by JVM.

-XX:+UseConcSweepGC (-XX:+UseParNewGC)
 parseParNew
 parseFullGC

-XX:+UseConcSweepGC -XX:CMSIncrementalMode (-XX:+UseParNewGC)
 parseParNew, parseFullGC,
 parse{InitialMark, MarkStart, Mark, PrecleanStart, Preclean,
       AbortablePrecleanStart, AbortablePreclean,
       AbortablePrecleanFullGC0, AbortablePrecleanFullGC1,
       AbortablePrecleanFailureTime,
       Remark,
       SweepStart, Sweep, ResetStart, Reset}
  parseAbortablePrecleanFullGC0 and parseAbortablePrecleanFullGC1
  must be always together.

-XX:+UseParallelGC
  parseParallelFullGC, parseParallelGC.

-XX:+UseSerialGC
  parseSerialFullGC, parseSerialGC.

"""
parseJavaGcLog = orP([
    parseDefaultGC,
    parseParNew,
    parseFullGC,
    parseInitialMark,
    parseMarkStart, parseMark,
    parsePrecleanStart, parsePreclean,
    parseAbortablePrecleanStart, parseAbortablePreclean,
    parseAbortablePrecleanFullGC0,
    parseAbortablePrecleanFullGC1,
    parseAbortablePrecleanFailureTime,
    parseRemark,
    parseSweepStart, parseSweep,
    parseResetStart, parseReset,
    parseParallelFullGC,
    parseParallelGC,
    parseSerialFullGC,
    parseSerialGC,
    ])

################################################################################
# Parser of list of integer. This is for test.
################################################################################

"""
A modifier for list.

return :: ([[String]], [String]) -> [String]

"""

def mkListAppender():
    def listAppend_(list, matchStringL):
        if len(matchStringL) > 0:
            list.append(matchStringL[0])
        return list

    return listAppend_


"""
Convert last element to Int.

list :: [Int, Int, ..., Int, String]
return :: [Int, Int, ..., Int, Int]

"""

def convertLastToInt(list):
    list[-1] = int(list[-1])
    return list

#75891.254: [GC [PSYoungGen: 40624K->886K(40640K)] 189358K->150201K(506688K), 0.0038020 secs]
class GCParser(object):
    @staticmethod
    def parse(lines,start=0,gcoptions=[]):
        parser=parseJavaGcLog
        if '+UseG1GC' in gcoptions:
            parser=parseG1GC
        datarray = []
        data_prev = None
        for line in lines:
            text = line.rstrip()
            try:
                # print text
                (ret, data) = parser(text, {})

                #UseGC1GC
                if data["type"] in ['pause','fullgc1']:
                    data_prev = data
                    parser = parseEden
                    continue

                if data["type"] == 'eden-heap':
                    assert data_prev["type"] in ['pause','fullgc1']
                    l_aux=data_prev["type"]
                    data_prev.update(data)
                    data_prev["type"]=l_aux
                    parser = parseTimes
                    continue

                if data["type"] == 'times':
                    assert data_prev["type"] in ['pause','fullgc1']
                    l_aux=data_prev["type"]
                    data_prev.update(data)
                    data = data_prev
                    data_prev = None
                    data["type"]=l_aux
                    parser = parseG1GC

                if  data["type"] == "CMS-concurrent-abortable-preclean-fullgc0":
                    data_prev = data
                    continue

                if data["type"] == "CMS-concurrent-abortable-preclean-fullgc1":
                    assert data_prev["type"] == "CMS-concurrent-abortable-preclean-fullgc0"
                    data_prev.update(data)
                    data = data_prev
                    data_prev = None
                    data["type"] = "CMS-concurrent-abortable-preclean-fullgc"

                #json.dumps(data)
                if 'timestamp' in data:
                    data['timestamp'] = int(data['timestamp'] + start)

                if data["type"].lower().find("fullgc")>=0:
                    data['type'] = "fullGC"
                else:
                    data['type'] = "minorGC"
                datarray.append(data)
            except ParseError as msg:
                # print msg
                LOG.debug("No parseado: %s", text,extra={'monitor': 'NA', 'modulo': "Gc"})
        return datarray
    # end of file.
