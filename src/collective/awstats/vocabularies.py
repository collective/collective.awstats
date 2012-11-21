from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from .interfaces import IAwstatsProvider
from . import _


def StandardPartsVocabulary(context):
    items = [
        ('General Overview', 'context/@@overview'),
        ('Month History', 'context/@@monthhistory'),
        ('Days in Month', 'context/@@daysinmonth'),
        ('Weekdays', 'context/@@weekdays'),
        ('Servertime', 'context/@@servertime'),
        ('Countries', 'context/@@countries'),
        ('Clients', 'context/@@clients'),
        ('Robots', 'context/@@robots'),
        ('Sessions', 'context/@@sessions'),
        ('Datatypes', 'context/@@datatypes'),
        ('Site URLs', 'context/@@siteurl'),
        ('Operating Systems', 'context/@@operatingsystems'),
        ('Browsers', 'context/@@browsers')]
    return SimpleVocabulary.fromItems(items)


directlyProvides(StandardPartsVocabulary, IVocabularyFactory)


def DomainVocabulary(context):
    domains = IAwstatsProvider(context).alloweddomains
    items = [(domain, domain) for domain in domains if domain]
    return SimpleVocabulary.fromItems(items)


directlyProvides(DomainVocabulary, IVocabularyFactory)


def EpochVocabulary(context):
    items = [
        (_(u'annual', u'Annual'), 'annual'),
        (_(u'monthly', u'Monthly'), 'monthly')]
    return SimpleVocabulary.fromItems(items)


directlyProvides(EpochVocabulary, IVocabularyFactory)
