from zope.interface import (
    Interface,
    Attribute,
)


class IAwstats(Interface):
    """Marker interface for .Awstats.Awstats
    """


class ICustomPart(Interface):
    """Marker interface for .CustomPart.CustomPart
    """


class IParsedStatistics(Interface):
    """Marker interface to make ParsedStatistics adaptable.
    """


class IParsedMonth(Interface):
    """Marker interface to make ParsedMonth adaptable.
    """


class IParsedSection(Interface):
    """Marker interface to make ParsedSection adaptable.
    """    


class IAwstatsProvider(Interface):
    """Class providing a ParsedStatistics object on demand.
    """
    
    statsavailable = Attribute("Flag if stats are available")
    
    alloweddomains = Attribute("The allowed domains")

    def getAvailableYears(domain):
        """Return the available years for given domain.
        """

    def getStatistics(domain):
        """returns the ParsedStatistics for given domain.
        """
 
    def reload(domain):
        """reload the statistics for given domain or reload all statistics
        if domain is None.
        """
