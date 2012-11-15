import calendar
from zope.interface import implementer
from interfaces import IDaysInMonth
from base import StatsBase
from collective.awstats.constants import *


@implementer(IDaysInMonth)
class DaysInMonth(StatsBase):
    """Implementation details see interfaces.IDaysInMonth
    """

    @property
    def daysinmonthgraph(self):
        data = self.getRawDayInMonthData()
        graph = dict()
        for set in data:
            graph[set['date']] = set['data']
        
        self.calculateGraphsData(graph, 60)
        for set in data:
            set['data'] = graph[set['date']]
        return data

    @property
    def daysinmonthbarnames(self):
        return ['visit', 'page', 'hit', 'byte']

    @property
    def daysinmonthoverview(self):
        data = self.getRawDayInMonthData()
        for set in data:
            set['data']['byte'] = self.parseBytes(set['data']['byte'])
        return data

    @property
    def daysinmonthaverage(self):
        data = self._getRawDayInMonthSum()
        days = calendar.mdays[11] # do some logic here
        for field in data.keys():
            data[field] = '%1.2f' % (float(data[field]) / days)
        data['byte'] = self.parseBytes(data['byte'])
        return data

    @property
    def daysinmonthsum(self):
        data = self._getRawDayInMonthSum()
        data['byte'] = self.parseBytes(data['byte'])
        return data

    def _getRawDayInMonthSum(self):
        data = self.getRawDayInMonthData()
        fields = self.daysinmonthbarnames
        summary = dict()
        for field in fields:
            summary[field] = 0
        for set in data:
            for field in fields:
                summary[field] += set['data'][field]
        
        return summary
