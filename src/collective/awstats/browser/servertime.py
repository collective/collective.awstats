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

from interfaces import IServertime
from base import StatsBase

from Products.BlueAwstats.constants import *

class Servertime(StatsBase):
    """Implementation details see interfaces.IServertime
    """
    
    implements(IServertime)
    
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

