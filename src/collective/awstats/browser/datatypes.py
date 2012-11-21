from zope.interface import implementer
from interfaces import IDatatypes
from base import StatsBase
from collective.awstats.constants import *


@implementer(IDatatypes)
class Datatypes(StatsBase):
    """Implementation details see interfaces.IDatatypes
    """

    @property
    def datatypesummary(self):
        my = self.my
        stats = self.stats[my]
        if not stats:
            rawdata = dict()
        else:
            rawdata = stats['FILETYPES']
        types = [ 'html', 'css', 'js', 'jpg', 'png',
                  'gif', 'pdf', 'doc', 'Unknown' ]
        totalhit = 0
        totalbyte = 0
        for type in types:
            typedata = rawdata.get(type, {})
            totalhit += int(typedata.get('hits', 0))
            totalbyte += int(typedata.get('bandwidth', 0))
        
        data = []
        for type in types:
            set = dict()
            typedata = rawdata.get(type, {})
            hit = int(typedata.get('hits', 0))
            hitpercent = self.calculateProportion(totalhit, hit) * 100
            byte = int(typedata.get('bandwidth', 0))
            bytepercent = self.calculateProportion(totalbyte, byte) * 100
            icon_tmpl = '++resource++collective.awstats.images/%s-ico.png'
            set['icon'] = icon_tmpl % type
            set['postfix'] = type
            set['filetype'] = FILETYPES[type]
            set['hit'] = hit
            set['hitpercent'] = '%1.2f %s' % (hitpercent, '%')
            set['byte'] = self.parseBytes(byte)
            set['bytepercent'] = '%1.2f %s' % (bytepercent, '%')
            data.append(set)
        return data
