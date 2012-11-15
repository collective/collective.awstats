# -*- coding: utf-8 -*-
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Robert Niederreiter <rnix@squarewave.at>"""
__docformat__ = 'plaintext'

from zope.interface import implements 

from interfaces import ICustomPart
from base import StatsBase

from Products.BlueAwstats.constants import *

class CustomPart(StatsBase):
    """Implementation details see interfaces.ICustomPart
    """
    
    implements(ICustomPart)
    
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
        if self.context.getGenerateGraph():
            count += 1
        return count
    
    @property
    def parttitle(self):
        my = self.my
        year = my[2:]
        epoch = self.context.getEpoch()
        if epoch == 'annual':
            epochtext = '(%s)' % year
        else:
            month = my[:2]
            epochtext = '(%s %s)' % (MONTH[month], year)
        title = self.context.Title()
        return '%s %s' % (title, epochtext)
    
    @property
    def customparthead(self):
        defs = self._partdefinitions
        head = [{}]
        if self.context.getGenerateGraph():
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
        epoch = self.context.getEpoch()
        if epoch == 'annual':
            data = self._annualcustompartdata
        else:
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
    def _annualcustompartdata(self):
        my = self.my
        year = my[2:]
        months = []
        query = self._generateQuery()
        for i in range(12):
            key = '%s%s' % (str(i + 1), year)
            if len(key) == 5:
                key = '0%s' % key
            stats = self.stats[key]
            if stats:
                months.append(self._getCustomPartData(stats['SIDER'], query))
        
        collectors = dict()
        orderedkeys = []
        for month in months:
            for row in month:
                title = row['title']
                collector = collectors.get(title)
                if not collector:
                    orderedkeys.append(title)
                    collectors[title] = {
                        'title': title,
                        'rendergraph': row['rendergraph'],
                        'columns': row['columns'],
                    }
                else:
                    pointer = 0
                    for col in row['columns']:
                        collector['columns'][pointer] += col
                        pointer += 1
        
        data = []
        for key in orderedkeys:
            data.append(collectors[key])
        return data
    
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
        rendergraph = self.context.getGenerateGraph()
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
    def _partdefinitions(self):
        if self.__partdefinitions is not False:
            return self.__partdefinitions
        
        defs = dict()
        defs['showgraph'] = self.context.getGenerateGraph()
        defs['epoch'] = self.context.getEpoch()
        defs['columns'] = []
        defs['rows'] = []
        
        structure = self.context.getDefinitions().split('\r\n')
        structure = [line.strip() for line in structure if line.strip()]
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
        ret = [definition.lower(), definition]
        if definition.find('(') != -1 and definition.find(')') != -1:
            ret[0] = definition[:definition.find('(')].strip().lower()
            ret[1] = definition[definition.find('('):].strip('()')
        return tuple(ret)
