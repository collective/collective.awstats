from zope.interface import implementer
from interfaces import IOverview
from .base import StatsBase
from collective.awstats.constants import MONTH


@implementer(IOverview)
class Overview(StatsBase):
    """Implementation details see interfaces.IOverview
    """

    @property
    def epoch(self):
        month = self.my[:2]
        year = self.my[2:]
        return '%s: %s %s' % ('Monat', MONTH[month], year)

    @property
    def firsttime(self):
        return self._getAccessTime('FirstTime')

    @property
    def lasttime(self):
        return self._getAccessTime('LastTime')

    @property
    def totalaverage(self):
        return self._calculateFloatAverage(self.totalunique(),
                                           self.totalvisits())

    @property
    def totalpagesaverage(self):
        return self._calculateFloatAverage(self.totalvisits(),
                                           self.totalknownpages())

    @property
    def totalhitsaverage(self):
        return self._calculateFloatAverage(self.totalvisits(),
                                           self.totalknownhits())

    @property
    def totalbytesaverage(self):
        total_bytes = self.getTotalRawBytes()
        visits = int(self.totalvisits())
        if visits == 0:
            return '0'
        average = total_bytes / visits
        return self.parseBytes(average)

    @property
    def totalunknownpages(self):
        return ''
        # later
        #stats = self.stats[self.my]
        #if not stats:
        #    return '0'
        #visitor = self.stats[self.my]['CLUSTER']
        #pages = 0
        #for key in visitor.keys():
        #    pages += int(visitor[key]['pages'])
        #return str(pages)

    @property
    def totalunknownhits(self):
        return str(self._countUnknown('hits'))

    @property
    def totalunknownbytes(self):
        return self.parseBytes(self._countUnknown('bandwidth'))

    def totalknownbytes(self, my=None):
        return self.parseBytes(self.getTotalRawBytes(my))

    def _getAccessTime(self, time):
        stats = self.stats[self.my]
        if not stats:
            return 'NA'
        date = stats['GENERAL'][time]
        if len(date) == 0:
            return 'NA'
        return self.parseDate(date[0])

    def _calculateFloatAverage(self, divisor, divident):
        divisor = float(divisor)
        divident = float(divident)
        if divisor == 0:
            return '0'
        average = divident / divisor
        return '%1.2f' % average

    def _countUnknown(self, datakey):
        stats = self.stats[self.my]
        if not stats:
            return '0'
        sections = ['ROBOT', 'WORMS', 'ERRORS']
        data = [self.stats[self.my][section] for section in sections]
        count = 0
        for d in data:
            if not d:
                continue
            for key in d.keys():
                count += int(d[key][datakey])
        return count
