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
import time
import calendar

from zope.interface import implements 
from Products.Five import BrowserView

from ZTUtils import make_query

from Products.CMFCore.utils import getToolByName

from interfaces import IStatsView
from base import StatsBase

from Products.BlueAwstats.constants import *
    
class StatsView(StatsBase):
    
    implements(IStatsView)
    
    partlinktitles = {
        'context/@@overview': 'Zusammenfassung',
        'context/@@monthhistory': 'Monatsübersicht',
        'context/@@daysinmonth': 'Tage im Monat',
        'context/@@weekdays': 'Wochentage',
        'context/@@servertime': 'Serverzeit',
        'context/@@countries': 'Domains/Länder',
        'context/@@clients': 'Rechner',
        'context/@@robots': 'Robots/Spiders',
        'context/@@sessions': 'Aufenthaltsdauer',
        'context/@@datatypes': 'Dateitypen',
        'context/@@siteurl': 'Seiten-URL',
        'context/@@operatingsystems': 'Betriebssysteme',
        'context/@@browsers': 'Browser',
    }
    
    """ LATER
    partlinkviews = {
        'overview': 'context/@@overview',
        'monthhistory': 'context/@@monthhistory',
        'daysinmonth': 'context/@@daysinmonth',
        'weekdays': 'context/@@weekdays',
        'servertime': 'context/@@servertime',
        'countries': 'context/@@countries',
        'clients': 'context/@@clients',
        'robots': 'context/@@robots',
        'sessions': 'context/@@sessions',
        'datatypes': 'context/@@datatypes',
        'siteurl': 'context/@@siteurl',
        'operatingsystems': 'context/@@operatingsystems',
        'browsers': 'context/@@browsers',
    }
    """
    
    @property
    def statsavailable(self):
        return self.provider.statsavailable
    
    @property
    def statsallowed(self):
        if not self.alloweddomains:
            return False
        return True
    
    @property
    def currentstaturl(self):
        return self.domain
    
    @property
    def displaygrouped(self):
        return self.context.getDisplaygrouped()
    
    @property
    def partlinks(self):
        parts = self._standardparts
        customparts = self._customparts
        parts += tuple([part[0] for part in customparts])
        if not parts:
            return []
        
        url = self.context.absolute_url()
        query = {
            'domain': self.domain,
            'currentmonth': self.request.get('currentmonth', ''),
            'currentyear': self.request.get('currentyear', ''),
        }
        currentpart = self.request.get('currentpart', '')
        if not currentpart:
            currentpart = parts[0]
        
        partlinks = []
        for part in parts:
            query.update({'currentpart': part})
            partlink = dict()
            title = self.partlinktitles.get(part)
            if not title:
                for cpart in customparts:
                    if cpart[0] == part:
                        title = cpart[1]
                        break
            if not title:
                title = part
            partlink['title'] = title
            partlink['url'] = '%s?%s' % (url, make_query(query))
            partlink['style'] = part == currentpart and 'currentItem' or None
            partlinks.append(partlink)
        return partlinks
    
    @property
    def statsparts(self):
        customparts = [part[0] for part in self._customparts]
        parts = self._standardparts + tuple(customparts)
        
        if self.context.getDisplaygrouped():
            return self._chooser + parts
            
        currentpart = self.request.get('currentpart', '')
        if not currentpart:
            currentpart = parts[0]
        
        return self._chooser + (currentpart,)
    
    def initialize(self):
        if self.request.get('reload', None):
            self.provider.reload(self.domain)
    
    @property
    def _chooser(self):
        return ('context/@@statschooser',)
    
    @property
    def _standardparts(self):
        return self.context.getStandardparts()
    
    @property
    def _customparts(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {
            'portal_type': 'CustomPart',
            'path': '/'.join(self.context.getPhysicalPath()),
            'getDomain': self.domain,
        }
        brains = catalog(**query)
        customparts = []
        for brain in brains:
            customparts.append(
                (
                    'context/%s/@@custompart' % brain.id,
                    brain.Title,
                )
            )
        return customparts

