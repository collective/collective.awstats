# -*- coding: utf-8 -*-
from zope.interface import implementer
from interfaces import IClients
from base import StatsBase
from collective.awstats.constants import *


@implementer(IClients)
class Clients(StatsBase):
    """Implementation details see interfaces.IClients
    """

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
