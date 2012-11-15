from zope.interface import implementer
from interfaces import ISiteURL
from base import StatsBase
from collective.awstats.constants import *


@implementer(ISiteURL)
class SiteURL(StatsBase):
    """Implementation details see interfaces.ISiteURL
    """

    @property
    def siteurlinfotext(self):
        my = self.my
        stats = self.stats[my]
        count = 0
        if stats:
            rawdata = stats['SIDER']
            count = len(rawdata.keys())
        text = '%i Unterschiedliche Seiten' % count
        return text

    @property
    def siteurldata(self):
        data = self._getOrderedSiteUrlData()
        graph = dict()
        for set in data:
            name = set['name']
            graph[name] = dict()
            graph[name]['hit'] = set['hit']
            graph[name]['sizeaverage'] = set['sizeaverage']
            graph[name]['entrance'] = set['entrance']
            graph[name]['exit'] = set['exit']
        
        self.calculateGraphsData(graph, 150)
        for set in data:
            set['sizeaverage'] = self.parseBytes(set['sizeaverage'])
            set['data'] = graph[set['name']]
        
        #do some request logic here
        if len(data) > 10:
            return data[:10]
        
        return data

    @property
    def siteurlbarnames(self):
        return [ 'hit', 'sizeaverage', 'entrance', 'exit' ]

    def _getOrderedSiteUrlData(self):
        ## TODO: simplify sorting
        my = self.my
        stats = self.stats[my]
        if not stats:
            return []
        rawdata = stats['SIDER']
        siteurls = rawdata.keys()
        sortlist = []
        for siteurl in siteurls:
            pages = rawdata[siteurl].get('pages', 0)
            sortlist.append(int(rawdata[siteurl]['pages']))
        sortlist.sort()
        sortlist.reverse()
        data = []
        for entry in sortlist:
            entry = str(entry)
            p = 0
            for siteurl in siteurls:
                if rawdata[siteurl]['pages'] == entry:
                    set = dict()
                    set['name'] = siteurl
                    hit = int(rawdata[siteurl].get('pages', 0))
                    set['hit'] = hit
                    byte = int(rawdata[siteurl].get('bandwidth'), 0)
                    set['sizeaverage'] = byte / hit
                    set['entrance'] = int(rawdata[siteurl].get('entry', 0))
                    set['exit'] = int(rawdata[siteurl].get('exit', 0))
                    siteurls.pop(p)
                    data.append(set)
                    break
                p += 1
        return data
