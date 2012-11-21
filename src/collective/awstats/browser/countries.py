import copy
from zope.interface import implementer
from interfaces import ICountries
from base import StatsBase
from collective.awstats.constants import *


@implementer(ICountries)
class Countries(StatsBase):
    """Implementation details see interfaces.ICountries
    """

    @property
    def countrydata(self):
        data = self._getOrderedDomainData()
        graph = dict()
        for set in data:
            graph[set['domain']] = copy.deepcopy(set['data'])
        
        self.calculateGraphsData(graph, 150)
        flag_tmpl = '++resource++collective.awstats.images/flags/flag-%s.gif'
        for set in data:
            set['flag'] = flag_tmpl % set['domain']
            set['country'] = DOMAINS.get(set['domain'].upper(), 'Undefined')
            set['text'] = set['data']
            set['text']['byte'] = self.parseBytes(set['data']['byte'])
            set['data'] = graph[set['domain']]
        
        #do some request logic here
        if len(data) > 10:
            return data[:10]
        
        return data

    @property
    def countrybarnames(self):
        return ['page', 'hit', 'byte']

    def _getOrderedDomainData(self):
        ## TODO: simplify sorting
        my = self.my
        stats = self.stats[my]
        if not stats:
            return []
        rawdata = stats['DOMAIN']
        domains = rawdata.keys()
        sortlist = []
        for domain in domains:
            sortlist.append(int(rawdata[domain]['pages']))
        sortlist.sort()
        sortlist.reverse()
        data = []
        for entry in sortlist:
            entry = str(entry)
            p = 0
            for domain in domains:
                if rawdata[domain]['pages'] == entry:
                    set = dict()
                    set['domain'] = domain
                    set['data'] = dict()
                    set['data']['page'] = int(rawdata[domain]['pages'])
                    set['data']['hit'] = int(rawdata[domain]['hits'])
                    set['data']['byte'] = int(rawdata[domain]['bandwidth'])
                    domains.pop(p)
                    data.append(set)
                    break
                p += 1
        return data
