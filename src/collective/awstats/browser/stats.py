# -*- coding: utf-8 -*-
import copy
import time
import calendar
from zope.interface import implementer
from Products.Five import BrowserView
from ZTUtils import make_query
from Products.CMFCore.utils import getToolByName
from interfaces import IStatsView
from base import StatsBase
from collective.awstats.constants import *


@implementer(IStatsView)
class StatsView(StatsBase):

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

        if self.displaygrouped:
            return self._chooser + parts

        currentpart = self.request.get('currentpart', '')
        if parts and not currentpart:
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


class ObjectStatsView(StatsView):

    @property
    def displaygrouped(self):
        return True

    @property
    def _standardparts(self):
        return ('context/@@contextstats',)

    @property
    def _customparts(self):
        return []
