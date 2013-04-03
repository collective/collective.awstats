from zope.interface import implementer
from zope.component import adapts
from Products.CMFCore import permissions
from Products.Archetypes import atapi
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.field import ExtensionField
from .. import _


class XBooleanField(ExtensionField, atapi.BooleanField): pass


@implementer(IOrderableSchemaExtender)
class AwstatsExtender(object):

    fields = [

        XBooleanField('awstats_enabled',
            schemata='settings',
            languageIndependent=True,
            default=True,
            write_permission=permissions.ModifyPortalContent,
            widget=atapi.BooleanWidget(
                label=_(u'awstats_label_enabled', u'Awstats erlauben'),
            ),
        ),

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, order):
        return order
