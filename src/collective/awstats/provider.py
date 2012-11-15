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

from interfaces import IAwstatsProvider

class AwstatsProvider(object):
    """Implementation details see interfaces.IAwstatsProvider.
    """
    
    implements(IAwstatsProvider)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def statsavailable(self):
        smt = self._getSmt()
        if not smt:
            return False
        return True
    
    @property
    def alloweddomains(self):
        smt = self._getSmt()
        if not smt:
            return []
        return smt.getAllowedDomains()
    
    def getAvailableYears(self, domain):
        smt = self._getSmt()
        if not smt:
            return []
        return smt.getAvailableYears(domain)
    
    def getStatistics(self, domain):
        smt = self._getSmt()
        return smt.getStatistics(domain)

    def reload(self, domain):
        smt = self._getSmt()
        smt.purge(domain)
    
    def _getSmt(self):
        try:
            return self.context.blueawstats_management_tool
        except:
            return None

