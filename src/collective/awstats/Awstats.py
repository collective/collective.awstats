# -*- coding: utf-8 -*-
#
# File: Awstats.py
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
from interfaces import IAwstats

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.BlueAwstats.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='standardparts',
        widget=MultiSelectionWidget(
            label='Standardparts',
            label_msgid='BlueAwstats_label_standardparts',
            i18n_domain='BlueAwstats',
        ),
        multiValued=1,
        vocabulary="getStandardPartsVocab"
    ),

    BooleanField(
        name='displaygrouped',
        widget=BooleanField._properties['widget'](
            label='Displaygrouped',
            label_msgid='BlueAwstats_label_displaygrouped',
            i18n_domain='BlueAwstats',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Awstats_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Awstats(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(IAwstats)
    meta_type = 'Awstats'
    _at_rename_after_creation = True

    schema = Awstats_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getStandardPartsVocab')
    def getStandardPartsVocab(self):
        vocab = (
            ('context/@@overview', 'General Overview'),
            ('context/@@monthhistory', 'Month History'),
            ('context/@@daysinmonth', 'Days in Month'),
            ('context/@@weekdays', 'Weekdays'),
            ('context/@@servertime', 'Servertime'),
            ('context/@@countries', 'Countries'),
            ('context/@@clients', 'Clients'),
            ('context/@@robots', 'Robots'),
            ('context/@@sessions', 'Sessions'),
            ('context/@@datatypes', 'Datatypes'),
            ('context/@@siteurl', 'Site URLs'),
            ('context/@@operatingsystems', 'Operating Systems'),
            ('context/@@browsers', 'Browsers'),
        )
        return vocab

    security.declarePublic('exclude_from_nav')
    def exclude_from_nav(self):
        return True


registerType(Awstats, PROJECTNAME)
# end of class Awstats

##code-section module-footer #fill in your manual code here
##/code-section module-footer



