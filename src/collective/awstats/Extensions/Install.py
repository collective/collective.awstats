# -*- coding: utf-8 -*-
#
# File: Install.py
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


from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from collective.awstats.config import PROJECTNAME

def install(self, reinstall=False):
    """External Method to install BlueAwstats 
    
    This method to install a product is kept, until something better will get
    part of Plones front end, which utilize portal_setup.
    """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    setuptool = getToolByName(self, 'portal_setup')
    oldcontext = setuptool.getImportContextID() 
    importcontext = 'profile-Products.%s:default' % PROJECTNAME
    setuptool.setImportContext(importcontext)
    setuptool.runAllImportSteps()
    setuptool.setImportContext(oldcontext)
    return out.getvalue()
