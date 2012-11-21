from zope.interface import implementer
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from ..interfaces import IAwstats
from .. import (
    config,
    _,
)


schema = atapi.Schema((

    atapi.LinesField(
        name='standardparts',
        widget=atapi.MultiSelectionWidget(
            label=_(u'awstats_label_standardparts', u'Standardparts'),
        ),
        multiValued=1,
        vocabulary_factory="collective.awstats.StandardPartsVocabulary",
    ),

    atapi.BooleanField(
        name='displaygrouped',
        widget=atapi.BooleanWidget(
            label=_(u'awstats_label_displaygrouped', u'Display grouped'),
        )
    ),

),
)


Awstats_schema = atapi.BaseFolderSchema.copy() + \
    schema.copy()


@implementer(IAwstats)
class Awstats(atapi.BaseFolder, BrowserDefaultMixin):
    security = ClassSecurityInfo()
    meta_type = 'Awstats'
    _at_rename_after_creation = True
    schema = Awstats_schema

    security.declarePublic('exclude_from_nav')
    def exclude_from_nav(self):
        return True


atapi.registerType(Awstats, config.PROJECTNAME)
