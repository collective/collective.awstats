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

from interfaces import ISessions
from base import StatsBase

from collective.awstats.constants import *

class Sessions(StatsBase):
    """Implementation details see interfaces.ISessions
    """
    
    implements(ISessions)
    
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

