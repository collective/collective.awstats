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

from interfaces import IClients
from base import StatsBase

from Products.BlueAwstats.constants import *

class Clients(StatsBase):
    """Implementation details see interfaces.IClients
    """
    
    implements(IClients)
    
    @property
    def clientsummarytext(self):
        params = {
            'known': self._getKnownClientsCount(),
            'unknown' : self._getUnknownClientsCount(),
        }
        text = """Rechner: %(known)s Bekannte, %(unknown)s Unbekannte 
                  (IP konnte nicht aufgelöst werden )
                """ % params
        return text
    
    @property
    def clientsummary(self):
        data = self._getOrderedClientData()
        for set in data:
            set['lastaccess'] = self.parseDate(set['lastaccess'])
            set['byte'] = self.parseBytes(set['byte'])
        
        #do some request logic here
        if len(data) > 10:
            return data[:10]
        
        return data
    
    def _getOrderedClientData(self):
        ## TODO: simplify sorting
        my = self.my
        stats = self.stats[my]
        if not stats:
            return []
        rawdata = stats['VISITOR']
        clients = rawdata.keys()
        
        sortlist = []
        for client in clients:
            sortlist.append(int(rawdata[client]['pages']))
        sortlist.sort()
        sortlist.reverse()
        data = []
        
        for entry in sortlist:
            entry = str(entry)
            p = 0
            for client in clients:
                if rawdata[client]['pages'] == entry:
                    clientdata = rawdata[client]
                    set = dict()
                    set['name'] = client
                    set['page'] = int(clientdata.get('pages', 0))
                    set['hit'] = int(clientdata.get('hits', 0))
                    set['byte'] = int(clientdata.get('bandwidth', 0))
                    set['lastaccess'] = clientdata.get('last visit date', '')
                    clients.pop(p)
                    data.append(set)
                    break
                p += 1
        return data
    
    def _getKnownClientsCount(self):
        data = self._getOrderedClientData()
        count = 0
        for set in data:
            client = set['name']
            if self._isClientKnown(client):
                count += 1
        return count
    
    def _isClientKnown(self, client):
        splitted = client.split('.')
        for part in splitted:
            if not part.isdigit():
                return True
        return False
    
    def _getUnknownClientsCount(self):
        data = self._getOrderedClientData()
        known = self._getKnownClientsCount()
        return len(data) - known

