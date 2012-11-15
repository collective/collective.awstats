# -*- coding: utf-8 -*-
#
# File: CustomPart.py
#
# Copyright (c) 2007 by BDA
# Generator: ArchGenXML Version 2.0-beta3 (dev/svn)
#            http://plone.org/products/archgenxml
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from interfaces import ICustomPart

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.BlueAwstats.config import *

##code-section module-header #fill in your manual code here
from Products.BlueAwstats.interfaces import IAwstatsProvider
##/code-section module-header

schema = Schema((

    StringField(
        name='domain',
        widget=SelectionWidget(
            label='Domain',
            label_msgid='BlueAwstats_label_domain',
            i18n_domain='BlueAwstats',
        ),
        vocabulary="getDomainVocab"
    ),

    StringField(
        name='epoch',
        widget=SelectionWidget(
            label='Epoch',
            label_msgid='BlueAwstats_label_epoch',
            i18n_domain='BlueAwstats',
        ),
        vocabulary="getEpochVocab"
    ),

    TextField(
        name='definitions',
        widget=TextAreaWidget(
            label='Definitions',
            label_msgid='BlueAwstats_label_definitions',
            i18n_domain='BlueAwstats',
        )
    ),

    BooleanField(
        name='generateGraph',
        widget=BooleanField._properties['widget'](
            label='Generategraph',
            label_msgid='BlueAwstats_label_generateGraph',
            i18n_domain='BlueAwstats',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CustomPart_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CustomPart(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(ICustomPart)
    meta_type = 'CustomPart'
    _at_rename_after_creation = True

    schema = CustomPart_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getEpochVocab')
    def getEpochVocab(self):
        return (('annual', 'Annual'), ('monthly', 'Monthly'))

    security.declarePublic('getDomainVocab')
    def getDomainVocab(self):
        return IAwstatsProvider(self).alloweddomains

    security.declarePublic('exclude_from_nav')
    def exclude_from_nav(self):
        return True


registerType(CustomPart, PROJECTNAME)
# end of class CustomPart

##code-section module-footer #fill in your manual code here
##/code-section module-footer



