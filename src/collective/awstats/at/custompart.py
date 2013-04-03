from zope.interface import implementer
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from ..interfaces import ICustomPart
from .. import (
    config,
    _,
)


schema = atapi.Schema((

    atapi.StringField(
        name='domain',
        widget=atapi.SelectionWidget(
            label=_(u'awstats_label_domain', u'Domain'),
        ),
        vocabulary_factory="collective.awstats.DomainVocabulary",
    ),

    atapi.TextField(
        name='definitions',
        widget=atapi.TextAreaWidget(
            label=_(u'awstats_label_definitions', u'Definitions'),
        )
    ),

    atapi.BooleanField(
        name='generateGraph',
        widget=atapi.BooleanWidget(
            label=_(u'awstats_label_generateGraph', u'Generategraph'),
        )
    ),

),
)


CustomPart_schema = atapi.BaseSchema.copy() + \
    schema.copy()


@implementer(ICustomPart)
class CustomPart(atapi.BaseContent, BrowserDefaultMixin):
    security = ClassSecurityInfo()
    meta_type = 'CustomPart'
    _at_rename_after_creation = True
    schema = CustomPart_schema

    security.declarePublic('exclude_from_nav')
    def exclude_from_nav(self):
        return True


atapi.registerType(CustomPart, config.PROJECTNAME)
