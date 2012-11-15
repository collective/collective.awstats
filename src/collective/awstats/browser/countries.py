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

import copy

from zope.interface import implements 

from interfaces import ICountries
from base import StatsBase

from collective.awstats.constants import *

class Countries(StatsBase):
    """Implementation details see interfaces.ICountries
    """
    
    implements(ICountries)
    
    @property
    def countrydata(self):
        data = self._getOrderedDomainData()
        graph = dict()
        for set in data:
            graph[set['domain']] = copy.deepcopy(set['data'])
        
        self.calculateGraphsData(graph, 150)
        for set in data:
            set['flag'] = 'flags/flag-%s.gif' % set['domain']
            set['country'] = DOMAINS.get(set['domain'].upper(), 'Undefined')
            set['text'] = set['data']
            set['text']['byte'] = self.parseBytes(set['data']['byte'])
            set['data'] = graph[set['domain']]
        
        #do some request logic here
        if len(data) > 10:
            return data[:10]
        
        return data
    
    @property
    def countrybarnames(self):
        return ['page', 'hit', 'byte']
    
    def _getOrderedDomainData(self):
        ## TODO: simplify sorting
        my = self.my
        stats = self.stats[my]
        if not stats:
            return []
        rawdata = stats['DOMAIN']
        domains = rawdata.keys()
        sortlist = []
        for domain in domains:
            sortlist.append(int(rawdata[domain]['pages']))
        sortlist.sort()
        sortlist.reverse()
        data = []
        for entry in sortlist:
            entry = str(entry)
            p = 0
            for domain in domains:
                if rawdata[domain]['pages'] == entry:
                    set = dict()
                    set['domain'] = domain
                    set['data'] = dict()
                    set['data']['page'] = int(rawdata[domain]['pages'])
                    set['data']['hit'] = int(rawdata[domain]['hits'])
                    set['data']['byte'] = int(rawdata[domain]['bandwidth'])
                    domains.pop(p)
                    data.append(set)
                    break
                p += 1
        return data
