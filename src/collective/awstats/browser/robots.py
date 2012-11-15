from zope.interface import implementer
from interfaces import IRobots
from base import StatsBase
from collective.awstats.constants import *


@implementer(IRobots)
class Robots(StatsBase):
    """Implementation details see interfaces.IRobots
    """

    @property
    def robotsummary(self):
        data = self._getOrderedRobotData()
        for set in data:
            set['lastaccess'] = self.parseDate(set['lastaccess'])
            set['byte'] = self.parseBytes(set['byte'])
        
        #do some request logic here
        if len(data) > 10:
            return data[:10]
        
        return data

    def _getOrderedRobotData(self):
        ## TODO: simplify sorting
        my = self.my
        stats = self.stats[my]
        if not stats:
            return []
        rawdata = stats['ROBOT']
        robots = rawdata.keys()
        
        sortlist = []
        for robot in robots:
            sortlist.append(int(rawdata[robot]['hits']))
        sortlist.sort()
        sortlist.reverse()
        data = []
        
        for entry in sortlist:
            entry = str(entry)
            p = 0
            for robot in robots:
                if rawdata[robot]['hits'] == entry:
                    robotdata = rawdata[robot]
                    set = dict()
                    set['name'] = robot
                    set['hit'] = int(robotdata.get('hits', 0))
                    set['byte'] = int(robotdata.get('bandwidth', 0))
                    set['lastaccess'] = robotdata.get('last visit', '')
                    robots.pop(p)
                    data.append(set)
                    break
                p += 1
        return data
