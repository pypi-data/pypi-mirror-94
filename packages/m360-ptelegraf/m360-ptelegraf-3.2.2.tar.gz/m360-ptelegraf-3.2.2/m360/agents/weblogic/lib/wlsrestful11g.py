import urllib2
import logging
import json
import time

DEFAULT_TIMEOUT = 305
EXPIRED_CACHE_SEGS=5

''' WLSRest class that encapsulate the monitoring methods,
authentication and GET call  ''' 
class WLS(object):

    def __init__(self, url,server,username, password, version='latest', verify=True,timeout=DEFAULT_TIMEOUT, servername=None):
        self._cache={}
        self._password=password
        self._username=username
        self._hostport=url
        self._server=server.split("/")[-1]
        self._baseURL = "%s/management/tenant-monitoring" % (url)
        data = self.get("servers/AdminServer")
        self._version = " ".join(data['body']['item']['weblogicVersion'].split("\n")[-1].split()[:3])

    @property
    def version(self):
        return self._version

    def get(self,uri):
        url=self._baseURL+"/"+uri
        #CACHEAMOS LAS PETICIONES
        if url in self._cache:
            #peticiones cacheada
            #tiempo transcurrido
            timestamp=self._cache[url]['time']
            now=time.time()
            if (now-timestamp) <= EXPIRED_CACHE_SEGS:
                self._cache[url]['time']=now
                return self._cache[url]['result']

        # HTTP Authentication
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, self._username, self._password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        
        try:
            data = ""
            req = urllib2.Request(url, None, {'Accept': 'application/json'})
            data = urllib2.urlopen(req).read()

            res=json.loads(data)
            self._cache[url]={'time':time.time(),'result':res}
            return res
            
        except urllib2.HTTPError, e:
            raise Exception("HTTP error: %d" % e.code)

        except urllib2.URLError, e:
            raise Exception("Network error: %s" % e.reason.args[1])
