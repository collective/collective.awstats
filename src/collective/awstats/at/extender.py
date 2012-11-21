from zope.interface import implements
from zope.component import adapts
from Products.CMFCore import permissions
from Products.Archetypes.utils import OrderedDict
from Products.Archetypes import atapi
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.field import ExtensionField
from .. import _


class XBooleanField(ExtensionField, atapi.BooleanField):
    pass


class XStringField(ExtensionField, atapi.StringField):
    pass


class AwstatsExtender(object):
    implements(IOrderableSchemaExtender)

    fields = [

        XBooleanField('awstats_enabled',
            schemata='settings',
            languageIndependent=True,
            write_permission=permissions.ModifyPortalContent,
            widget=atapi.BooleanWidget(
                label=_(u'awstats_label_enabled', u'Awstats erlauben'),
            ),
        ),

        XStringField('awstats_domain',
            schemata='settings',
            languageIndependent=True,
            write_permission=permissions.ModifyPortalContent,
            widget=atapi.SelectionWidget(
                label=_(u'awstats_label_domain', u'Awstats Domain'),
            ),
            vocabulary_factory="collective.awstats.DomainVocabulary",
        ),

        XStringField('awstats_epoch',
            schemata='settings',
            languageIndependent=True,
            write_permission=permissions.ModifyPortalContent,
            widget=atapi.SelectionWidget(
                label=_(u'awstats_label_epoch', u'Awstats Epoch'),
            ),
            vocabulary_factory="collective.awstats.EpochVocabulary",
        ),

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, original):
        neworder = OrderedDict()
        keys = original.keys()
        last = keys.pop()
        keys.insert(1, last)
        for schemata in keys:
            neworder[schemata] = original[schemata]
        return neworder
