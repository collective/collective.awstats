from zope.interface import implementer
from interfaces import IStatsChooser
from base import StatsBase
from collective.awstats.constants import *


@implementer(IStatsChooser)
class StatsChooser(StatsBase):
    """Implementation details see interfaces.IStatsChooser
    """

    @property
    def form_action(self):
        return self.context.absolute_url()

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


class ObjectStatsChooser(StatsChooser):

    @property
    def form_action(self):
        return '%s/@@object_stats' % self.context.absolute_url()
