from zope.interface import implementer
from interfaces import IServertime
from base import StatsBase
from collective.awstats.constants import *


@implementer(IServertime)
class Servertime(StatsBase):
    """Implementation details see interfaces.IServertime
    """

    @property
    def servertimegraph(self):
        data = self._getRawServertimeData()
        graph = dict()
        for set in data:
            graph[set['hour']] = set['data']
        
        self.calculateGraphsData(graph, 60)
        for set in data:
            set['data'] = graph[set['hour']]
        return data

    @property
    def servertimebarnames(self):
        return ['page', 'hit', 'byte']

    @property
    def servertimeoverview(self):
        data = self._getRawServertimeData()
        for set in data:
            set['data']['byte'] = self.parseBytes(set['data']['byte'])
        return data

    def _getRawServertimeData(self):
        my = self.my
        hours = HOURS
        setdataFields = ['page', 'hit', 'byte']
        statFields = ['pages', 'hits', 'bandwidth']
        
        hoursums = dict()
        for hour in hours:
            hoursums[hour] = dict()
            for field in statFields:
                value = self._getFieldForServertime(my, hour, field)
                hoursums[hour][field] = value
        
        data = []
        for hour in hours:
            set = dict()
            set['hour'] = hour
            set['data'] = dict()
            p = 0
            for field in setdataFields:
                value = hoursums[hour][statFields[p]]
                set['data'][field] = value
                p += 1
            data.append(set)
        return data

    def _getFieldForServertime(self, my, hour, field):
        my = self.currentMy(my)
        stats = self.stats[my]
        if not stats:
            return 0
        data = stats['TIME'].get(hour)
        if data:
            field = data.get(field)
            if field:
                return int(field)
        return 0
