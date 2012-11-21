from zope.interface import implementer
from interfaces import IOperatingSystems
from base import StatsBase
from collective.awstats.constants import *


@implementer(IOperatingSystems)
class OperatingSystems(StatsBase):
    """Implementation details see interfaces.IOperatingSystems
    """

    @property
    def ossummary(self):
        my = self.my
        stats = self.stats[my]
        if not stats:
            rawdata = dict()
        else:
            rawdata = stats['OS']
        total = { 'win': 0, 'mac': 0, 'linux': 0, 'Unknown': 0 }
        for os in rawdata.keys():
            for prefix in total.keys():
                if os.startswith(prefix):
                    total[prefix] += int(rawdata[os].get('hits', 0))
                    break
        
        totalsum = 0
        for key in total.keys():
            totalsum += total[key]

        data = []
        oskeys = ['win', 'mac', 'linux', 'Unknown']
        for os in oskeys:
            set = dict()
            icon_tmpl = '++resource++collective.awstats.images/%s-ico.png'
            set['icon'] = icon_tmpl % os
            set['name'] = OS_FAMILIES[os]
            hit = total[os] 
            set['hit'] = hit
            hitpercent = self.calculateProportion(totalsum, hit) * 100
            set['hitpercent'] = '%1.2f %s' % (hitpercent, '%')
            data.append(set)
        return data
