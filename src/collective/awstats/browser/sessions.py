from zope.interface import implementer
from interfaces import ISessions
from base import StatsBase
from collective.awstats.constants import *


@implementer(ISessions)
class Sessions(StatsBase):
    """Implementation details see interfaces.ISessions
    """

    @property
    def sessionsummary(self):
        my = self.my
        stats = self.stats[my]
        if not stats:
            rawdata = dict()
        else:
            rawdata = stats['SESSION']
            
        ranges = [ '0s-30s', '30s-2mn', '2mn-5mn', '5mn-15mn', 
                   '15mn-30mn', '30mn-1h', '1h+' ]
        
        total = int(self.totalvisits())
        known = 0
        for range in ranges:
            rangedata = rawdata.get(range, {})
            known += int(rangedata.get('number of visits', 0))
        unknown = total - known
            
        data = []
        for range in ranges:
            set = dict()
            rangedata = rawdata.get(range, {})
            visits = int(rangedata.get('number of visits', 0))
            percent = self.calculateProportion(total, visits) * 100
            set['name'] = range
            set['count'] = visits
            set['percent'] = '%1.2f %s' % (percent, '%')
            data.append(set)
        set = dict()
        percent = self.calculateProportion(total, unknown) * 100
        set['name'] = 'Unbekannt'
        set['count'] = unknown
        set['percent'] = '%1.2f %s' % (percent, '%')
        data.append(set)
        return data
