from zope.interface import implementer
from interfaces import IOperatingSystems
from base import StatsBase
from collective.awstats.constants import OS_FAMILIES


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
        total = {'win': 0, 'mac': 0, 'linux': 0, 'Unknown': 0}
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
            record = dict()
            icon_tmpl = '++resource++collective.awstats.images/%s-ico.png'
            record['icon'] = icon_tmpl % os
            record['name'] = OS_FAMILIES[os]
            hit = total[os]
            record['hit'] = hit
            hitpercent = self.calculateProportion(totalsum, hit) * 100
            record['hitpercent'] = '%1.2f %s' % (hitpercent, '%')
            data.append(record)
        return data
