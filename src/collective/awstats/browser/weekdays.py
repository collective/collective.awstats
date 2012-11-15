# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from zope.interface import implements 

from interfaces import IWeekdays
from base import StatsBase

from collective.awstats.constants import *

class Weekdays(StatsBase):
    """Implementation details see interfaces.IWeekdays
    """
    
    implements(IWeekdays)
    
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
    
