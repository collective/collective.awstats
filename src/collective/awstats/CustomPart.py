from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implementer
from interfaces import ICustomPart
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from collective.awstats.config import *
from collective.awstats.interfaces import IAwstatsProvider


schema = Schema((

    StringField(
        name='domain',
        widget=SelectionWidget(
            label='Domain',
            label_msgid='awstats_label_domain',
            i18n_domain='awstats',
        ),
        vocabulary="getDomainVocab"
    ),

    StringField(
        name='epoch',
        widget=SelectionWidget(
            label='Epoch',
            label_msgid='awstats_label_epoch',
            i18n_domain='awstats',
        ),
        vocabulary="getEpochVocab"
    ),

    TextField(
        name='definitions',
        widget=TextAreaWidget(
            label='Definitions',
            label_msgid='awstats_label_definitions',
            i18n_domain='awstats',
        )
    ),

    BooleanField(
        name='generateGraph',
        widget=BooleanField._properties['widget'](
            label='Generategraph',
            label_msgid='awstats_label_generateGraph',
            i18n_domain='awstats',
        )
    ),

),
)


CustomPart_schema = BaseSchema.copy() + \
    schema.copy()


@implementer(ICustomPart)
class CustomPart(BaseContent, BrowserDefaultMixin):
    security = ClassSecurityInfo()
    meta_type = 'CustomPart'
    _at_rename_after_creation = True
    schema = CustomPart_schema

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
