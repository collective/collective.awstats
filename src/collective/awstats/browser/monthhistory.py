from zope.interface import implementer
from interfaces import IMonthHistory
from base import StatsBase
from collective.awstats.constants import MONTH


@implementer(IMonthHistory)
class MonthHistory(StatsBase):
    """Implementation details see interfaces.IMonthHistory
    """

    @property
    def monthgraph(self):
        data = self._getRawMonthData(self.my[2:])
        graph = dict()
        for record in data:
            graph[set['month']] = record['data']

        self.calculateGraphsData(graph, 100)
        for record in data:
            record['data'] = graph[record['month']]
        return data

    @property
    def monthbarnames(self):
        return ['unique', 'visit', 'page', 'hit', 'byte']

    @property
    def monthoverview(self):
        data = self._getRawMonthData(self.my[2:])
        for record in data:
            record['data']['byte'] = self.parseBytes(record['data']['byte'])
        return data

    @property
    def monthsum(self):
        data = self._getRawMonthData(self.my[2:])
        fields = self.monthbarnames
        summary = dict()
        for field in fields:
            summary[field] = 0
        for record in data:
            for field in fields:
                summary[field] += record['data'][field]
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
            rset = dict()
            rset['month'] = '%s %s' % (MONTH[m], year)
            rset['data'] = dict()
            rset['data']['unique'] = int(self.totalunique(my))
            rset['data']['visit'] = int(self.totalvisits(my))
            rset['data']['page'] = int(self.totalknownpages(my))
            rset['data']['hit'] = int(self.totalknownhits(my))
            rset['data']['byte'] = self.getTotalRawBytes(my)
            data.append(rset)
        return data
