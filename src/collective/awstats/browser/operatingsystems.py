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

from interfaces import IOperatingSystems
from base import StatsBase

from Products.BlueAwstats.constants import *

class OperatingSystems(StatsBase):
    """Implementation details see interfaces.IOperatingSystems
    """
    
    implements(IOperatingSystems)
    
    @property
    def ossummary(self):
        my = self.my
        stats = self.stats[my]
        if not stats:
            rawdata = dict()
        else:
            rawdata = stats['OS']
        total = { 'win': 0, 'mac': 0, 'linux': 0, 'Unknown': 0 }
        for os in rawdata.keys():
            for prefix in total.keys():
                if os.startswith(prefix):
                    total[prefix] += int(rawdata[os].get('hits', 0))
                    break
        
        totalsum = 0
        for key in total.keys():
            totalsum += total[key]

        data = []
        oskeys = ['win', 'mac', 'linux', 'Unknown']
        for os in oskeys:
            set = dict()
            set['icon'] = '%s-ico.png' % os
            set['name'] = OS_FAMILIES[os]
            hit = total[os] 
            set['hit'] = hit
            hitpercent = self.calculateProportion(totalsum, hit) * 100
            set['hitpercent'] = '%1.2f %s' % (hitpercent, '%')
            data.append(set)
        return data

