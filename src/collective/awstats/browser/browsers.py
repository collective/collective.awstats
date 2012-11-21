from zope.interface import implementer
from interfaces import IBrowsers
from base import StatsBase
from collective.awstats.constants import *


@implementer(IBrowsers)
class Browsers(StatsBase):
    """Implementation details see interfaces.IOperatingSystems
    """

    @property
    def browsersummary(self):
        my = self.my
        stats = self.stats[my]
        if not stats:
            rawdata = dict()
        else:
            rawdata = stats['BROWSER']
        
        browserfamilies = BROWSER_FAMILIES.keys()
        
        total = dict()
        for browser in browserfamilies:
            total[browser] = 0
        
        for browser in rawdata.keys():
            for prefix in total.keys():
                if browser.startswith(prefix):
                    total[prefix] += int(rawdata[browser].get('hits', 0))
                    break
        
        totalsum = 0
        for key in total.keys():
            totalsum += total[key]

        data = []
        for browser in browserfamilies:
            set = dict()
            icon_tmpl = '++resource++collective.awstats.images/%s-ico.png'
            set['icon'] = icon_tmpl % browser
            set['name'] = BROWSER_FAMILIES[browser]
            hit = total[browser] 
            set['hit'] = hit
            hitpercent = self.calculateProportion(totalsum, hit) * 100
            set['hitpercent'] = '%1.2f %s' % (hitpercent, '%')
            data.append(set)
        return data
