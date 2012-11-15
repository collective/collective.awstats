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

from interfaces import IStatsChooser
from base import StatsBase

from Products.BlueAwstats.constants import *

class StatsChooser(StatsBase):
    """Implementation details see interfaces.IStatsChooser
    """
    
    implements(IStatsChooser)
    
    @property    
    def lastmodified(self):
        stats = self.stats[self.my]
        if not stats:
            return 'NA'
        date = stats['GENERAL']['LastUpdate'][0]
        return self.parseDate(date)
    
    @property
    def monthselection(self):
        return MONTH_TUPLES
    
    @property
    def yearselection(self):
        return self.provider.getAvailableYears(self.domain)
    
    def domainSelected(self, domain):
        if domain == self.domain:
            return True
        return False
    
    def monthSelected(self, month):
        m = self.my[:2]
        if m == month:
            return True
        return False
    
    def yearSelected(self, year):
        y = self.my[2:]
        if y == year:
            return True
        return False
    