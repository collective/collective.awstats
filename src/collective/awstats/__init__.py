from zope.i18nmessageid import MessageFactory
from Products.CMFCore import utils
from Products.Archetypes import atapi
from . import config


_ = MessageFactory(config.PROJECTNAME)


def initialize(context):
    """Register content types through Archetypes with Zope and the CMF.
    """
    from at import (
        awstats,
        custompart,
    )

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit("%s: %s" % (config.PROJECTNAME, atype.portal_type),
            content_types      = (atype,),
            permission         = config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)
