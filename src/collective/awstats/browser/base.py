import copy
import time
import calendar
from Products.Five import BrowserView
from collective.awstats.interfaces import IAwstatsProvider
from collective.awstats.constants import *


class StatsBase(BrowserView):
    """Base for stats.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self._stats = False
        self._domain = False
        self._my = False
        self._provider = False

    @property
    def provider(self):
        if self._provider is not False:
            return self._provider
        self._provider = IAwstatsProvider(self.context)
        return self._provider

    @property
    def alloweddomains(self):
        """The currently alowed domains
        """
        return self.provider.alloweddomains

    @property
    def stats(self):
        """The current statistics.
        """
        if self._stats is False:
            self._stats = self.provider.getStatistics(self.domain)
        return self._stats

    @property
    def domain(self):
        """The currently used domain.
        
        Reads domain from request and checks against the allowed domains
        for this user / site.
        """
        if self._domain is False:
            allowed = self.alloweddomains
            domain = self.request.get('domain')
            if not domain or not domain in allowed:
                self._domain = allowed[0]
            else:
                self._domain = domain
        return self._domain

    @property
    def my(self):
        """Allocate month/year for this request.
        
        Try to get month/year from request, if successless return curren month
        and year.
        """
        if self._my is not False:
            return self._my
        
        req = self.request
        month = req.get('currentmonth', None)
        year = req.get('currentyear', None)
        if not month or not year:
            lt = time.localtime()
            month = str(lt[1])
            year = str(lt[0])
            if len(month) == 1:
                month = '0%s' % month
        self._my = '%s%s' % (month, year)
        return self._my

    def currentMy(self, my):
        """Check if month / year is not the default for this request.
        
        Needed for the month overview statistics f.e."""
        if my is None:
            return self.my
        return my

    def getTotalRawBytes(self, my=None):
        """Return the total raw bytes for this month.
        """
        bytes = 0
        my = self.currentMy(my)
        stats = self.stats[my]
        if not stats:
            return bytes
        days = stats['DAY']
        for key in days.keys():
            bytes += int(days[key]['bandwidth'])
        return bytes

    def totalunique(self, my=None):
        return self._countGeneralTotal('TotalUnique', my)

    def totalvisits(self, my=None):
        return self._countGeneralTotal('TotalVisits', my)

    def totalknownpages(self, my=None):
        return self._countTotalKnown('pages', my)

    def totalknownhits(self, my=None):
        return self._countTotalKnown('hits', my)

    def getRawDayInMonthData(self):
        my = self.my
        mdays = self._getMdaysFor(my)
        data = []
        dateday = 1
        for day in mdays:
            set = dict()
            set['date'] = self._getDateForDay(my, dateday)
            set['dateday'] = str(dateday)
            set['weekday'] = DAYS[day]
            set['data'] = dict()
            set['data']['visit'] = self._getFieldForDay(my, dateday, 'visits')
            set['data']['page'] = self._getFieldForDay(my, dateday, 'pages')
            set['data']['hit'] = self._getFieldForDay(my, dateday, 'hits')
            set['data']['byte'] = self._getFieldForDay(my, dateday, 'bandwidth')
            if day == 5 or day == 6:
                set['highlight'] = True
            else:
                set['highlight'] = False
            data.append(set)
            dateday += 1
        
        return data

    def parseDate(self, date, longformat=True):
        """Parse given date and return readable output.
        """
        if not date:
            return ''
        year = date[:4]
        month = date[4:6]
        day = date[6:8]
        if longformat:
            hour = date[8:10]
            minute = date[10:12]
            return '%s.%s.%s - %s:%s' % (day, month, year, hour, minute)
        return '%s.%s.%s' % (day, month, year)

    def parseBytes(self, bytes):
        unit = 0
        volume = float(bytes)
        while True:
            if volume / 1024 < 1:
                return '%1.2f%s' % (volume, DATA_UNITS[unit])
            volume = volume / 1024
            unit += 1

    def calculateProportion(self, par, comp):
        par = float(par)
        comp = float(comp)
        if par == 0:
            return 0
        return comp / par

    def calculateGraphsData(self, data, size):
        """data is a dict withs graphs.
        
        size is the max size for a bar in pixel
        every graph is a dict itself with the bars
        the graphs inside data must have the same structure.
        """
        if not data:
            return None
        
        graphs = data.keys()
        maxvalues = dict()
        for bar in data[graphs[0]].keys():
            maxvalues[bar] = 0
        
        for graph in graphs:
            for bar in data[graph].keys():
                value = data[graph][bar]
                if value > maxvalues[bar]:
                    maxvalues[bar] = value
        
        for graph in graphs:
            self._calculateGraphData(data[graph], size, maxvalues)

    def _countGeneralTotal(self, datakey, my):
        my = self.currentMy(my)
        stats = self.stats[my]
        if stats:
            return stats['GENERAL'][datakey][0]
        return '0'

    def _countTotalKnown(self, datakey, my):
        my = self.currentMy(my)
        stats = self.stats[my]
        if not stats:
            return '0'
        days = stats['DAY']
        count = 0
        for key in days.keys():
            count += int(days[key][datakey])
        return str(count)

    def _getMdaysFor(self, my):
        month = int(my[:2])
        year = int(my[2:])
        wdays = calendar.monthcalendar(year, month)
        mdays = []
        for week in wdays:
            wday = 0
            for day in week:
                if day > 0:
                    mdays.append(wday)
                wday += 1
        return mdays

    def _getDateForDay(self, my, day):
        date = self._getRawDate(my, day)
        return self.parseDate(date, longformat=False)

    def _getFieldForDay(self, my, day, field):
        my = self.currentMy(my)
        stats = self.stats[my]
        if not stats:
            return 0
        data = stats['DAY'].get(self._getRawDate(my, day))
        if data:
            field = data.get(field)
            if field:
                return int(field)
        return 0

    def _getRawDate(self, my, day):
        my = str(my)
        day = str(day)
        year = my[2:]
        month = my[:2]
        if len(day) == 1:
            day = '0%s' % day
        return '%s%s%s' % (year, month, day)

    def _calculateGraphData(self, graph, size, maxvalues):
        bars = graph.keys()
        for bar in bars:
            prop = self.calculateProportion(maxvalues[bar], graph[bar])
            graph[bar] = int(size * prop)
