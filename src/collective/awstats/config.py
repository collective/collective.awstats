from Products.CMFCore.permissions import setDefaultRoles
from bda.awstatsparser.defaults import *


PROJECTNAME = "collective.awstats"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'Awstats': 'awstats: Add Awstats',
    'CustomPart': 'awstats: Add CustomPart',
}

setDefaultRoles('awstats: Add Awstats', ('Manager', 'Owner'))
setDefaultRoles('awstats: Add CustomPart', ('Manager', 'Owner'))

product_globals = globals()
