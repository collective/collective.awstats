from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implementer
from interfaces import IAwstats
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from collective.awstats.config import *


schema = Schema((

    LinesField(
        name='standardparts',
        widget=MultiSelectionWidget(
            label='Standardparts',
            label_msgid='awstats_label_standardparts',
            i18n_domain='awstats',
        ),
        multiValued=1,
        vocabulary="getStandardPartsVocab"
    ),

    BooleanField(
        name='displaygrouped',
        widget=BooleanField._properties['widget'](
            label='Displaygrouped',
            label_msgid='awstats_label_displaygrouped',
            i18n_domain='awstats',
        )
    ),

),
)


Awstats_schema = BaseFolderSchema.copy() + \
    schema.copy()


@implementer(IAwstats)
class Awstats(BaseFolder, BrowserDefaultMixin):
    security = ClassSecurityInfo()
    meta_type = 'Awstats'
    _at_rename_after_creation = True
    schema = Awstats_schema

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
