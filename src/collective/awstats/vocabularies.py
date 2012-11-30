from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from .interfaces import IAwstatsProvider
from . import _


def StandardPartsVocabulary(context):
    items = [
        (_(u'general_overview', u'General Overview'), 'context/@@overview'),
        (_(u'month_history', 'Month History'), 'context/@@monthhistory'),
        (_(u'days_in_month', u'Days in Month'), 'context/@@daysinmonth'),
        (_(u'weekdays', u'Weekdays'), 'context/@@weekdays'),
        (_(u'servertime', u'Servertime'), 'context/@@servertime'),
        (_(u'countries', u'Countries'), 'context/@@countries'),
        (_(u'clients', u'Clients'), 'context/@@clients'),
        (_(u'robots', u'Robots'), 'context/@@robots'),
        (_(u'sessions', u'Sessions'), 'context/@@sessions'),
        (_(u'datatypes', u'Datatypes'), 'context/@@datatypes'),
        (_(u'site_urls', u'Site URLs'), 'context/@@siteurl'),
        (_(u'oper_sys', u'Operating Systems'), 'context/@@operatingsystems'),
        (_(u'browsers', u'Browsers'), 'context/@@browsers')]
    return SimpleVocabulary.fromItems(items)


directlyProvides(StandardPartsVocabulary, IVocabularyFactory)


def DomainVocabulary(context):
    domains = IAwstatsProvider(context).alloweddomains
    items = [(domain, domain) for domain in domains if domain]
    return SimpleVocabulary.fromItems(items)


directlyProvides(DomainVocabulary, IVocabularyFactory)
