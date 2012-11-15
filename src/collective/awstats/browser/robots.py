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

from interfaces import IRobots
from base import StatsBase

from Products.BlueAwstats.constants import *

class Robots(StatsBase):
    """Implementation details see interfaces.IRobots
    """
    
    implements(IRobots)
    
    @property
    def robotsummary(self):
        data = self._getOrderedRobotData()
        for set in data:
            set['lastaccess'] = self.parseDate(set['lastaccess'])
            set['byte'] = self.parseBytes(set['byte'])
        
        #do some request logic here
        if len(data) > 10:
            return data[:10]
        
        return data
    
    def _getOrderedRobotData(self):
        ## TODO: simplify sorting
        my = self.my
        stats = self.stats[my]
        if not stats:
            return []
        rawdata = stats['ROBOT']
        robots = rawdata.keys()
        
        sortlist = []
        for robot in robots:
            sortlist.append(int(rawdata[robot]['hits']))
        sortlist.sort()
        sortlist.reverse()
        data = []
        
        for entry in sortlist:
            entry = str(entry)
            p = 0
            for robot in robots:
                if rawdata[robot]['hits'] == entry:
                    robotdata = rawdata[robot]
                    set = dict()
                    set['name'] = robot
                    set['hit'] = int(robotdata.get('hits', 0))
                    set['byte'] = int(robotdata.get('bandwidth', 0))
                    set['lastaccess'] = robotdata.get('last visit', '')
                    robots.pop(p)
                    data.append(set)
                    break
                p += 1
        return data
    