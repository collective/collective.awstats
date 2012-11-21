from Products.CMFCore.permissions import setDefaultRoles


PROJECTNAME = "collective.awstats"
ADD_PERMISSIONS = {
    'Awstats': 'collective.awstats: Add Awstats',
    'CustomPart': 'collective.awstats: Add CustomPart',
}

setDefaultRoles('collective.awstats: Add Awstats', ('Manager', 'Owner'))
setDefaultRoles('collective.awstats: Add CustomPart', ('Manager', 'Owner'))
