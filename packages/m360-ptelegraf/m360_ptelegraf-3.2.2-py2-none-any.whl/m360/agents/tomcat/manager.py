# -*- coding: utf-8 -*-
import requests
import bs4
import re
import m360.base.manager as base
from logging import getLogger

LOG=getLogger('m360.agents.tomcat')

requests.packages.urllib3.disable_warnings()


class Manager(base.Manager):

    @staticmethod
    def list_processes(text_url, username, password):
        '''
        This function queries the Tomcat Manager for a list of running
        Tomcat container processes.
        :param:
        :returns: a dict of process information. Keys are the contxt paths; values
            are also dictionaries with uniform keys 'running'(boolean),
            'session_count'(int), and 'context_path'(string).
        :raises:

        '''
        url = text_url + '/text/list'
        session = requests.Session()
        session.verify = False
        resp = session.get(url, auth=(username, password))
        resp.raise_for_status()
        # construct dict of dicts
        processes_by_context = {}
        for line in resp.text.split('\n'):
            if line.startswith('/'):
                segments = line.split(':')
                # context path as key
                context = segments[0]
                # dict of segment name/values
                val = {}
                val['running'] = segments[1] and segments[1] == 'running'
                val['session_count'] = int(segments[2])
                val['context_path'] = segments[3]
                # make dict entry
                processes_by_context[context] = val
        return processes_by_context

    @staticmethod
    def server_info(text_url, username, password):
        uris = {'/text/serverinfo': Manager.server_info_tomcat8,  # TOMCAT8,
                '/html': Manager.server_info_tomcat5  # TOMCAT5
                }

        resp = None
        for uri in uris:
            url = text_url + uri
            try:
                session = requests.Session()
                session.verify = False
                resp = session.get(url, auth=(username, password))
                resp.raise_for_status()
                break  # La primera url que responda la pillamos
            except requests.HTTPError as e:
                LOG.warning("No se pudo conectar con el endpoint: %s, error: %s", url, e.message,
                                extra=Manager.getcaller())
                resp = None
                pass
            except requests.ConnectionError as e:
                LOG.warning("No se pudo conectar con el endpoint: %s, error: %s", url, e.message,
                                extra=Manager.getcaller())
                resp = None
                pass

        return uris[uri](resp.text, resp.encoding) if resp else {}

    @staticmethod
    def server_info_tomcat5(text, encode):
        servinfo = {}
        # scrape the HTML
        soup = bs4.BeautifulSoup(text, "html.parser")
        tables = soup.find_all('table')
        # TOMCAT5
        # TOMCAT8
        lasttable = tables[-1:][0]
        lines = Manager.scrape_table_rows(lasttable)
        for i in range(len(lines[1])):
            var = lines[1][i]
            servinfo[var.strip()] = lines[2][i].strip()
        return servinfo

    @staticmethod
    def server_info_tomcat8(text, encode):
        servinfo = {}
        lines = text.split('\n')
        if lines[0].startswith('OK -'):
            for line in lines[1:]:
                parts = line.split(':')
                # lines without one ':' should be ignored
                if len(parts) > 1:
                    if len(parts) > 2:
                        # there was an extra colon in the value.
                        # Rebuild the value
                        parts = [parts[0], ':'.join(parts[1:])]
                    servinfo[parts[0].strip()] = parts[1].strip()
        return servinfo

    @staticmethod
    def server_resources(text_url, username, password):
        uris = {'/text/resources': Manager.jndi_resources,  # TOMCAT8,
                '/resources': Manager.jndi_resources  # TOMCAT5
                }

        resp = None
        for uri in uris:
            url = text_url + uri
            try:
                session = requests.Session()
                session.verify = False
                resp = session.get(url, auth=(username, password))
                resp.raise_for_status()
                break  # La primera url que responda la pillamos
            except requests.HTTPError as e:
                LOG.warning("No se pudo conectar con el endpoint: %s, error: %s", url, e.message,
                                extra=Manager.getcaller())
                resp = None
                pass
            except requests.ConnectionError as e:
                LOG.warning("No se pudo conectar con el endpoint: %s, error: %s", url, e.message,
                                extra=Manager.getcaller())
                resp = None
                pass

        return uris[uri](resp.text) if resp else {}

    @staticmethod
    def jndi_resources(text):
        jndis = text.split('\n')
        if jndis[0].startswith('OK -'):
            if len(jndis) == 1:
                return []
            else:
                return jndis[1:]

    @staticmethod
    def find_named_sibling(tag, desired_name, how_many_tries=5, beforetag=None):
        '''
        Convenience method. Given a BeautifulSoup tag, finds the first occurrence
        of the desired_name in a sibling tag. Will look for up to how_many_tries.
        '''
        sib = tag
        for indx in range(how_many_tries):
            if sib.next_sibling:
                sib = sib.next_sibling
                if sib.name == desired_name:
                    return sib
                if beforetag:
                    if sib.name == beforetag:
                        return None
            else:
                print('Out of siblings at ' + str(indx) + '. wtf.')
                return None

    @staticmethod
    def scrape_table_rows(tbl, filt=None):
        '''
        Walks through the rows of a table. If a given row is not eliminated
        by filter function 'filt', the row is converted into a list of string
        values of the th or td tags in the row.

        The 'filt' function must return True if the row is desired, else False.
        '''
        retrows = []
        rows = tbl.find_all('tr')
        if filt:
            rows = [row for row in rows if filt(row)]
        for row in rows:
            retrows.append([cell.string.strip() for cell in row.find_all(['td', 'th'])])
        return retrows

    @staticmethod
    def scrape_paragraph(p, filt=None):
        '''
        Walks through the words of a paragrah. If a given row is not eliminated
        by filter function 'filt', the row is converted into a list of string
        values of the th or td tags in the row.

        The 'filt' function must return True if the row is desired, else False.
        '''
        retrows = {}
        factors = {"MB": 1024 * 1024, "KB": 1024, "GB": 1024 * 1204 * 1024, "B": 1}

        # field : value [MB|KB|GB|B]"
        for text in p.contents:
            if type(text) != bs4.NavigableString:
                continue
            if text != "":
                text = text.replace(":", " : ")
                arraytext = text.split()
                field = ""
                value = ""
                fieldcomplete = False
                for word in arraytext:
                    if word != ":" and word not in ["MB", "KB", "GB", "B"]:
                        if fieldcomplete and value == "":
                            value = word
                        else:
                            if value != "":
                                retrows[field] = value
                                value = ""
                                field = ""
                                fieldcomplete = False
                            field = field + word.capitalize()
                    elif word == ":":
                        fieldcomplete = True
                    else:
                        value = float(value) * factors[word]
                        fieldcomplete = False
                        retrows[field] = value
                        field = ""
                        value = ""

                if value != "":
                    retrows[field] = value

        return retrows

    @staticmethod
    def skip_ready_threads(row):
        '''
        Filter method: returns True IFF the parameter has a first cell that does
        not contain the string value "R". Intended to eliminate thread table
        rows that are in "Ready" state (i.e., not working.)
        :param row: A beautiful soup tag for an HTML row
        :returns: False if the parameter is None, has no first cell, or has a
            first cell with string value "R"; else True
        '''
        if row:
            firstcell = row.find(['th', 'td'])
            if firstcell:
                firstcontent = firstcell.string
                return firstcontent != 'R'
            else:
                return False
        else:
            return False

    @staticmethod
    def server_jmx(status_url, username, password, metrics=True, rootnode="Catalina", beanname="", **kargs):
        data = {}
        extrarrgs = ",".join([arg + "=" + value if value != "*" else "*" for (arg, value) in kargs.iteritems()])
        args = "{0}:type={1},{2}".format(rootnode, beanname, extrarrgs)
        try:
            session = requests.Session()
            session.verify = False
            LOG.debug("Llamando al jmxproxy: %s", status_url + "/jmxproxy?qry=" + args, extra=Manager.getcaller())
            resp = session.get(status_url + "/jmxproxy", params={"qry": args}, auth=(username, password))
            resp.raise_for_status()
        except Exception as e:
            LOG.error("Error al invocar al jmxproxy: %s,Error: %s", status_url + "/jmxproxy?qry=" + args,
                          str(e), extra=Manager.getcaller())
            return data
        if resp.content.startswith("OK"):
            text = resp.content.replace("\r", "").split("\n")
            indexes = [i for i in range(len(text)) if text[i].startswith("Name:")]
            indexes.append(len(text) - 1)
            beanblocks = [text[indexes[x]:indexes[x + 1]] for x in range(len(indexes) - 1)]
            for bean in beanblocks:
                if bean[0].startswith("Name"):
                    m = re.search(r'name="?([^\s,"]+)"?', bean[0], re.IGNORECASE)
                    if m:
                        name = m.group(1)
                    else:
                        m = re.search(r'host=([^\s,]+)', bean[0], re.IGNORECASE)
                        if m:
                            name = m.group(1)
                        else:
                            break

                data[name] = {}
                for j in range(1, len(bean)):
                    if bean[j] == "":
                        continue
                    if bean[j].startswith("modeler"):
                        continue
                    keyvalue = bean[j].split(":")
                    if (len(keyvalue) > 1):
                        key = keyvalue[0].strip()
                        try:
                            if metrics:
                                val = float(keyvalue[1].strip())
                            else:
                                val = keyvalue[1].strip()
                            data[name][key] = val
                        except Exception as e:
                            pass
        return data

    @staticmethod
    def server_status(status_url, username, password):
        session = requests.Session()
        session.verify = False
        resp = session.get(status_url + "/status", auth=(username, password))
        resp.raise_for_status()

        # scrape the HTML
        soup = bs4.BeautifulSoup(resp.text, "html.parser")

        # html headers are defined as header name (page content) and filter (function)
        header_defs = {r"JVM": None,
                       r"http": Manager.skip_ready_threads,
                       r"jk": Manager.skip_ready_threads,
                       r"ajp": Manager.skip_ready_threads}

        hdrs = soup.find_all('h1')
        headertables = {}
        for hdr in hdrs:
            # TOMCAT 8 con "
            headername = str(hdr.string).replace('"', '')

            headers = [(headername, h) for h in header_defs if re.match(h, headername)]
            if headers:
                p = Manager.find_named_sibling(hdr, 'p')
                if p:
                    data = Manager.scrape_paragraph(p, filt=header_defs[headers[0][1]])
                    headertables[headers[0][0]] = data

                # TOMCAT 8x: Memory Pool.
                if headername == "JVM":
                    table = Manager.find_named_sibling(hdr, 'table', beforetag="h1")
                    if table:
                        headertables["MemoryPool"] = []
                        lines = Manager.scrape_table_rows(table)
                        if len(lines) > 1:
                            for j in range(len(lines) - 1):
                                metricas = {}
                                for i in range(len(lines[0])):
                                    metricas[lines[0][i].replace(' ', '')] = Manager.to_bytes(lines[j + 1][i])
                                headertables["MemoryPool"].append(metricas)

        return headertables

    @staticmethod
    def to_bytes(value):
        ret2 = 0
        ret = value.replace(' ', '')
        ret = re.sub("\(.*\)", "", ret)
        if re.search("[0-9](MB|KB|GB|B)$", ret):
            factor = 1
            if ret.endswith("MB"):
                factor = 1024 * 1024
            elif ret.endswith("KB"):
                factor = 1024
            elif ret.endswith("GB"):
                factor = 1024 * 1024 * 1024

            try:
                ret = float(re.sub("[A-Za-z]", "", ret)) * factor
            except Exception as e:
                return ret

        return ret
