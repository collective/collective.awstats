from zope.interface import implementer
from interfaces import IMonthHistory
from base import StatsBase
from collective.awstats.constants import *

@implementer(IMonthHistory)
class MonthHistory(StatsBase):
    """Implementation details see interfaces.IMonthHistory
    """

    @property
    def monthgraph(self):
        data = self._getRawMonthData(self.my[2:])
        graph = dict()
        for set in data:
            graph[set['month']] = set['data']
            
        self.calculateGraphsData(graph, 100)
        for set in data:
            set['data'] = graph[set['month']]
        return data

    @property
    def monthbarnames(self):
        return ['unique', 'visit', 'page', 'hit', 'byte']

    @property
    def monthoverview(self):
        data = self._getRawMonthData(self.my[2:])
        for set in data:
            set['data']['byte'] = self.parseBytes(set['data']['byte'])
        return data

    @property
    def monthsum(self):
        data = self._getRawMonthData(self.my[2:])
        fields = self.monthbarnames
        summary = dict()
        for field in fields:
            summary[field] = 0
        for set in data:
            for field in fields:
                summary[field] += set['data'][field]
        summary['byte'] = self.parseBytes(summary['byte'])
        return summary

    def _getRawMonthData(self, year):
        """Return the raw (not formatted) general data for this month.
        """
        data = []
        month = MONTH.keys()
        month.sort()
        
        for m in month:
            my = '%s%s' % (m, year)
            set = dict()
            set['month'] = '%s %s' % (MONTH[m], year)
            set['data'] = dict()
            set['data']['unique'] = int(self.totalunique(my))
            set['data']['visit'] = int(self.totalvisits(my))
            set['data']['page'] = int(self.totalknownpages(my))
            set['data']['hit'] = int(self.totalknownhits(my))
            set['data']['byte'] = self.getTotalRawBytes(my)
            data.append(set)
        return data
