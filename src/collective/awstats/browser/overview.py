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

from interfaces import IOverview
from base import StatsBase

from Products.BlueAwstats.constants import *

class Overview(StatsBase):
    """Implementation details see interfaces.IOverview
    """
    
    implements(IOverview)
    
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
        bytes = self.getTotalRawBytes()
        visits = int(self.totalvisits())
        if visits == 0:
            return '0'
        average = bytes / visits
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
    