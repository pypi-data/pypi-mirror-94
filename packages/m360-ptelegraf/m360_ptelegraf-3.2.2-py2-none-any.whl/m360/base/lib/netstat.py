import pwd
import os
import re
import glob
from collections import namedtuple


class Netstat():
    def __init__(self):
        pass

    PROC_TCP = "/proc/net/tcp"
    PROC_UDP = "/proc/net/udp"
    STATE = {
            '01':'ESTABLISHED',
            '02':'SYN_SENT',
            '03':'SYN_RECV',
            '04':'FIN_WAIT1',
            '05':'FIN_WAIT2',
            '06':'TIME_WAIT',
            '07':'CLOSE',
            '08':'CLOSE_WAIT',
            '09':'LAST_ACK',
            '0A':'LISTEN',
            '0B':'CLOSING'
            }

    @staticmethod
    def _load(type='tcp'):
        ''' Read the table of tcp connections & remove header  '''
        if type=='udp':
            file = Netstat.PROC_UDP
        else:
            file = Netstat.PROC_TCP

        with open(file,'r') as f:
            content = f.readlines()
            content.pop(0)
        return content

    @staticmethod
    def _hex2dec(s):
        return str(int(s,16))

    @staticmethod
    def _ip(s):
        ip = [(Netstat._hex2dec(s[6:8])),(Netstat._hex2dec(s[4:6])),(Netstat._hex2dec(s[2:4])),(Netstat._hex2dec(s[0:2]))]
        return '.'.join(ip)

    @staticmethod
    def _remove_empty(array):
        return [x for x in array if x !='']

    @staticmethod
    def _convert_ip_port(array):
        host,port = array.split(':')
        return Netstat._ip(host),Netstat._hex2dec(port)

    @staticmethod
    def netstat(type="tcp"):
        '''
        Function to return a list with status of tcp connections at linux systems
        To get pid of all network process running on system, you must run this script
        as superuser
        '''

        content=Netstat._load(type)
        result = []
        for line in content:
            line_array = Netstat._remove_empty(line.split(' '))     # Split lines and remove empty spaces.
            l_host,l_port = Netstat._convert_ip_port(line_array[1]) # Convert ipaddress and port from hex to decimal.
            r_host,r_port = Netstat._convert_ip_port(line_array[2])
            tcp_id = line_array[0]
            state = Netstat.STATE[line_array[3]]
            uid = pwd.getpwuid(int(line_array[7]))[0]       # Get user from UID.
            inode = line_array[9]                           # Need the inode to get process pid.
            pid = Netstat._get_pid_of_inode(inode)                  # Get pid prom inode.
            try:                                            # try read the process name.
                exe = os.readlink('/proc/'+pid+'/exe')
            except:
                exe = None
            socket = namedtuple('Socket',['id','uid','local','remote','status','pid','process'])
            nline = socket(tcp_id, uid, l_host+':'+l_port, r_host+':'+r_port, state, pid if pid else "", exe if exe else "")
            result.append(nline)
        return result

    @staticmethod
    def _get_pid_of_inode(inode):
        '''
        To retrieve the process pid, check every running process and look for one using
        the given inode.
        '''
        for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
            try:
                if re.search(inode,os.readlink(item)):
                    return item.split('/')[2]
            except:
                pass
        return None
