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

from interfaces import IMonthHistory
from base import StatsBase

from collective.awstats.constants import *

class MonthHistory(StatsBase):
    """Implementation details see interfaces.IMonthHistory
    """
    
    implements(IMonthHistory)
    
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
