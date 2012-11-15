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

from interfaces import IDatatypes
from base import StatsBase

from collective.awstats.constants import *

class Datatypes(StatsBase):
    """Implementation details see interfaces.IDatatypes
    """
    
    implements(IDatatypes)
    
    @property
    def datatypesummary(self):
        my = self.my
        stats = self.stats[my]
        if not stats:
            rawdata = dict()
        else:
            rawdata = stats['FILETYPES']
        types = [ 'html', 'css', 'js', 'jpg', 'png',
                  'gif', 'pdf', 'doc', 'Unknown' ]
        totalhit = 0
        totalbyte = 0
        for type in types:
            typedata = rawdata.get(type, {})
            totalhit += int(typedata.get('hits', 0))
            totalbyte += int(typedata.get('bandwidth', 0))
        
        data = []
        for type in types:
            set = dict()
            typedata = rawdata.get(type, {})
            hit = int(typedata.get('hits', 0))
            hitpercent = self.calculateProportion(totalhit, hit) * 100
            byte = int(typedata.get('bandwidth', 0))
            bytepercent = self.calculateProportion(totalbyte, byte) * 100
            set['icon'] = '%s-ico.png' % type
            set['postfix'] = type
            set['filetype'] = FILETYPES[type]
            set['hit'] = hit
            set['hitpercent'] = '%1.2f %s' % (hitpercent, '%')
            set['byte'] = self.parseBytes(byte)
            set['bytepercent'] = '%1.2f %s' % (bytepercent, '%')
            data.append(set)
        return data

