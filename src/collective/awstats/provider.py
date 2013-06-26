import os
import logging
from zope.interface import implementer
from zope.annotation import IAnnotations
from zope.component import getUtility
from persistent.dict import PersistentDict
from Acquisition import (
    aq_inner,
    aq_parent,
)
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.registry.interfaces import IRegistry
from bda.awstatsparser.parser import ParsedStatistics
from bda.awstatsparser.defaults import SECTIONDEFS
from .interfaces import IAwstatsProvider


logger = logging.getLogger('collective.awstats')


def lookup_site_root(context):
    context = aq_inner(context)
    while context and not IPloneSiteRoot.providedBy(context):
        context = aq_parent(context)
    return context


@implementer(IAwstatsProvider)
class AwstatsProvider(object):

    def __init__(self, context):
        self.context = lookup_site_root(context)

    @property
    def registry(self):
        return getUtility(IRegistry)

    @property
    def basedir(self):
        return self.registry['collective.awstats.basedir']

    @property
    def prefix(self):
        return self.registry['collective.awstats.prefix']

    @property
    def postfix(self):
        return self.registry['collective.awstats.postfix']

    @property
    def statistics(self):
        annotations = IAnnotations(self.context)
        if not 'awstats' in annotations:
            annotations['awstats'] = PersistentDict()
        return annotations['awstats']

    @property
    def statsavailable(self):
        return os.path.exists(self.basedir)

    @property
    def alloweddomains(self):
        return self.registry['collective.awstats.domains']

    def reload(self, domain):
        if not domain:
            self.statistics.clear()
        else:
            try:
                del self.statistics[domain]
            except KeyError, e:
                logger.warning(str(e))

    def getAvailableYears(self, currentdomain):
        if not self.statsavailable:
            return []
        dircontents = os.listdir(self.basedir)
        files = []
        for entry in dircontents:
            if not os.path.isdir(entry):
                files.append(entry)
        domains = self.alloweddomains
        years = []
        for filename in files:
            if not filename.startswith(self.prefix) \
              or not filename.endswith(self.postfix):
                continue
            domain = filename[len(self.prefix) + \
                              7:filename.index('.%s' % self.postfix)]
            year = filename[len(self.prefix) + 2:len(self.prefix) + 6]
            if not year in years \
              and domain in domains \
              and domain == currentdomain:
                years.append(year)
        return years

    def readStatistics(self, domain):
        if self.statsavailable:
            directory = self.basedir
            pre = self.prefix
            post = self.postfix
            stats = ParsedStatistics(domain, directory, pre, post, SECTIONDEFS)
            self.statistics[domain] = stats

    def getStatistics(self, domain):
        stats = self.statistics.get(domain)
        if not stats:
            self.readStatistics(domain)
        return self.statistics.get(domain)

    def listAvailableDomains(self):
        if not self.statsavailable:
            return []
        dircontents = os.listdir(self.basedir)
        files = []
        for entry in dircontents:
            if not os.path.isdir(entry):
                files.append(entry)
        domains = []
        for filename in files:
            if not filename.startswith(self.prefix) \
              or not filename.endswith(self.postfix):
                continue
            start = len(self.prefix) + 7
            end = filename.index('.%s' % self.postfix)
            domain = filename[start:end]
            if not domain in domains:
                domains.append(domain)
        return domains
