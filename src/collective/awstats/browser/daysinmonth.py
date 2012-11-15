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

import calendar

from zope.interface import implements 

from interfaces import IDaysInMonth
from base import StatsBase

from Products.BlueAwstats.constants import *

class DaysInMonth(StatsBase):
    """Implementation details see interfaces.IDaysInMonth
    """
    
    implements(IDaysInMonth)
    
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
    
