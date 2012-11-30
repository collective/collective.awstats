from zope.interface import implementer
from Acquisition import (
    aq_inner,
    aq_parent,
)
from Products.CMFPlone.interfaces import IPloneSiteRoot
from interfaces import (
    ICustomPart,
    IContextStats,
)
from base import StatsBase
from collective.awstats.constants import *


@implementer(ICustomPart)
class CustomPart(StatsBase):
    """Implementation details see interfaces.ICustomPart
    """

    barnamemapping = {
        'pages': 'hit',
        'bandwidth': 'byte',
        'entry': 'entrance',
        'exit': 'exit',
    }

    def __init__(self, context, request):
        super(CustomPart, self).__init__(context, request)
        self.__partdefinitions = False
        self.__custompartbarnames = False

    @property
    def columncount(self):
        count = len(self.custompartbarnames) + 1
        if self._generategraph:
            count += 1
        return count

    @property
    def parttitle(self):
        my = self.my
        year = my[2:].decode('utf-8')
        month = my[:2].decode('utf-8')
        return u'%s %s' % (self.context.Title().decode('utf-8'),
                           u'(%s %s)' % (MONTH[month], year))

    @property
    def customparthead(self):
        defs = self._partdefinitions
        head = [{}]
        if self._generategraph:
            head.append({})
        
        barnamekeys = self.barnamemapping.keys()
        for col in defs['columns']:
            if col[0] in barnamekeys:
                head.append({
                    'title': col[1],
                    'style': '%scolor datacolumn' % self.barnamemapping[col[0]],
                })
        return head

    @property
    def custompartdata(self):
        data = self._monthlycustompartdata
        barnames = self.custompartbarnames
        graphs = dict()
        for dataset in data:
            graph = dict()
            pointer = 0
            for barname in barnames:
                graph[barname] = dataset['columns'][pointer]
                pointer += 1
            graphs[dataset['title']] = graph
        
        self.calculateGraphsData(graphs, 150)
        
        for dataset in data:
            dataset['data'] = graphs[dataset['title']]
            pointer = 0
            for col in dataset['columns']:
                if barnames[pointer] == 'byte':
                    bytes = dataset['columns'][pointer]
                    bytes = self.parseBytes(bytes)
                    dataset['columns'][pointer] = bytes
                pointer += 1
        
        return data

    @property
    def custompartbarnames(self):
        if self.__custompartbarnames is not False:
            return self.__custompartbarnames
        defs = self._partdefinitions
        barnames = []
        barnamekeys = self.barnamemapping.keys()
        for col in defs['columns']:
            if col[0] in barnamekeys:
                barnames.append(self.barnamemapping[col[0]])
        
        self.__custompartbarnames = barnames
        return self.__custompartbarnames

    @property
    def _monthlycustompartdata(self):
        my = self.my
        stats = self.stats[my]
        if not stats:
            stats = dict()
        rawdata = stats.get('SIDER', dict())
        return self._getCustomPartData(rawdata, self._generateQuery())

    def _generateQuery(self):
        defs = self._partdefinitions
        keys = self.barnamemapping.keys()
        query = dict()
        query['cols'] = [col[0] for col in defs['columns'] if col[0] in keys]
        query['rows'] = list()
        for row in defs['rows']:
            query['rows'].append(row)
        return query

    def _getCustomPartData(self, rawdata, query):
        rendergraph = self._generategraph
        data = list()
        for row in query['rows']:
            rowdata = rawdata.get(row[0])
            dataset = dict()
            dataset['title'] = row[1]
            dataset['rendergraph'] = rendergraph
            dataset['columns'] = list()
            for col in query['cols']:
                if not rowdata:
                    dataset['columns'].append(0)
                else:
                    dataset['columns'].append(int(rowdata.get(col, 0)))
            data.append(dataset)
        return data

    @property
    def _generategraph(self):
        return self.context.getGenerateGraph()

    @property
    def _structure(self):
        structure = self.context.getDefinitions().split('\r\n')
        structure = [line.strip() for line in structure if line.strip()]
        return structure

    @property
    def _partdefinitions(self):
        if self.__partdefinitions is not False:
            return self.__partdefinitions
        
        defs = dict()
        defs['showgraph'] = self._generategraph
        defs['columns'] = []
        defs['rows'] = []
        
        structure = self._structure
        if not structure:
            return defs
        
        cols = []
        for definition in structure[0].split('|'):
            cols.append(self._getDefinition(definition))
        defs['columns'] = cols
        
        if len(structure) < 2:
            return defs
        rows = []
        for definition in structure[1:]:
            rows.append(self._getDefinition(definition))
        defs['rows'] = rows
        
        return defs

    def _getDefinition(self, definition):
        definition = definition.strip()
        ret = [definition, definition]
        if definition.find('(') != -1 and definition.find(')') != -1:
            ret[0] = definition[:definition.find('(')].strip()
            ret[1] = definition[definition.find('('):].strip('()')
        return tuple(ret)


@implementer(IContextStats)
class ContextStats(CustomPart):
    """Implementation details see interfaces.ICustomPart
    """

    @property
    def _generategraph(self):
        return True

    @property
    def _objectpath(self):
        context = aq_inner(self.context)
        path = list()
        while not IPloneSiteRoot.providedBy(context):
            path.append(context.getId())
            context = aq_parent(context)
        path = reversed(path)
        return '/' + '/'.join(path)

    @property
    def _structure(self):
        defs = 'pages (Zugriffe) | bandwidth (Bytes) | ' +\
               'entry (Einstieg) | exit (Exit)'
        path = self._objectpath + ' (Angezeigtes Objekt)'
        return [defs, path]
