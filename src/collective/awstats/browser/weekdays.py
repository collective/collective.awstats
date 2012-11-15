from zope.interface import implementer
from interfaces import IWeekdays
from base import StatsBase
from collective.awstats.constants import *


@implementer(IWeekdays)
class Weekdays(StatsBase):
    """Implementation details see interfaces.IWeekdays
    """

    @property
    def weekdaysgraph(self):
        data = self._getRawWeekdaysData()
        graph = dict()
        for set in data:
            graph[set['day']] = set['data']
        
        self.calculateGraphsData(graph, 60)
        for set in data:
            set['data'] = graph[set['day']]
        return data

    @property
    def weekdaysbarnames(self):
        return ['page', 'hit', 'byte']

    @property
    def weekdaysoverview(self):
        data = self._getRawWeekdaysData()
        for set in data:
            set['data']['byte'] = self.parseBytes(set['data']['byte'])
        return data

    def _getRawWeekdaysData(self):
        rawdata = self.getRawDayInMonthData()        
        weekdays = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        setdataFields = self.weekdaysbarnames
        weekdaysums = dict()
        for weekday in weekdays:
            weekdaysums[weekday] = dict()
            for field in setdataFields:
                weekdaysums[weekday][field] = 0
            weekdaysums[weekday]['count'] = 0.0
        
        for set in rawdata:
            setdata = set['data']
            for field in setdataFields:
                weekdaysums[set['weekday']][field] += setdata[field]
            weekdaysums[set['weekday']]['count'] += 1
        
        data = []
        for day in weekdays:
            set = dict()
            set['day'] = day
            set['data'] = dict()
            for field in setdataFields:
                value = weekdaysums[day][field] / weekdaysums[day]['count']
                set['data'][field] = value
            if day == 'Sa' or day == 'So':
                set['highlight'] = True
            else:
                set['highlight'] = False
            data.append(set)   
        return data
