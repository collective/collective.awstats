from zope.interface import (
    Interface,
    Attribute,
)


class IStatsView(Interface):
    """Interface definition for the statistics view class.
    """

    statsavailable = Attribute("Flag if stats are available")

    statsallowed = Attribute("Flag if stats are allowed")

    currentstaturl = Attribute("The current displayed stats url")

    displaygrouped = Attribute("Flag wether to display the parts grouped")

    partlinks = Attribute("The links to the parts")

    statsparts = Attribute("The parts to display")

    def initialize():
        """Checks for stat reload. has to be removed in future
        """


class IStatsChooser(Interface):
    """View class interface for the stats chooser.
    """

    lastmodified = Attribute("Date when stats has been last modified")

    alloweddomains = Attribute("Allowed domains definitions")

    monthselection = Attribute("The month selection definitions")

    yearselection = Attribute("The Year selection definitions")

    def domainSelected(domain):
        """Return wether domain is selected or not.
        """

    def monthSelected(month):
        """Return wether month is selected or not.
        """

    def yearSelected(year):
        """Return wether year is selected ot not.
        """


class IOverview(Interface):
    """View class interface for the stats overview.
    """

    epoch = Attribute("The displayed epoch")

    firsttime = Attribute("Time of first access")

    lasttime = Attribute("Time of last access")

    totalaverage = Attribute("Total visits average")

    totalpagesaverage = Attribute("Total known pages average")

    totalhitsaverage = Attribute("Total known hits average")

    totalbytesaverage = Attribute("Total known bytes average")

    totalunknownpages = Attribute("Total unknown pages count")

    totalunknownhits = Attribute("Total unknown hits count")

    totalunknownbytes = Attribute("Total unknown bytes count")

    def totalunique(my=None):
        """Total unique visitor count
        """

    def totalvisits(my=None):
        """Total visits count
        """

    def totalknownpages(my=None):
        """Total known pages count.
        """

    def totalknownhits(my=None):
        """Total known hits count.
        """

    def totalknownbytes(my=None):
        """Total known bytes count.
        """


class IMonthHistory(Interface):
    """Interface definition for the month history view class.
    """

    monthgraph = Attribute("Data for the month graphs")

    monthbarnames = Attribute("The barnames for the month graph")

    monthoverview = Attribute("The month overview data")

    monthsum = Attribute("The month sum data")


class IDaysInMonth(Interface):
    """Interface definition for the days in month view class.
    """

    daysinmonthgraph = Attribute("Data for the days in month graphs")

    daysinmonthbarnames = Attribute("The bar names for the graphs")

    daysinmonthoverview = Attribute("The overview data")

    daysinmonthaverage = Attribute("The days in month average")

    daysinmonthsum = Attribute("The days in month sum")


class IWeekdays(Interface):
    """Interface definition for the weekdays view class.
    """

    weekdaysgraph = Attribute("Data for the weekdays graphs")

    weekdaysbarnames = Attribute("The bar names for the graphs")

    weekdaysoverview = Attribute("The overview data")


class IServertime(Interface):
    """Interface definition for the servertime view class.
    """

    servertimegraph = Attribute("Data for the servertime graphs")

    servertimebarnames = Attribute("The bar names for the graphs")

    servertimeoverview = Attribute("The overview data")


class ICountries(Interface):
    """Interface definition for the countries view class.
    """

    countrydata = Attribute("The countires data")

    countrybarnames = Attribute("The bar names fot the graphs")


class IClients(Interface):
    """Interface definition for the clients view class.
    """

    clientsummarytext = Attribute("The infotext")

    clientsummary = Attribute("The client summary data")


class IRobots(Interface):
    """Interface definition for the robots view class.
    """

    robotsummary = Attribute("The robot summary data")


class ISessions(Interface):
    """Interface definition for the sessions view class.
    """

    sessionsummary = Attribute("The session summary data")


class IDatatypes(Interface):
    """Interface definition for the datatypes view class.
    """

    datatypesummary = Attribute("The datatype summary")


class ISiteURL(Interface):
    """Interface definition for the site url view class.
    """

    siteurlinfotext = Attribute("The site url infotext")

    siteurldata = Attribute("The site url data")

    siteurlbarnames = Attribute("The bar names of the graphs")


class IOperatingSystems(Interface):
    """Interface definition for the operating systems view class.
    """

    ossummary = Attribute("The operating system summary data")


class IBrowsers(Interface):
    """Interface definition for the browsers view class.
    """

    browsersummary = Attribute("The browsers summary")


class ICustomPart(Interface):
    """Interface definition for the custom part view class.
    """

    columncount = Attribute("The number of displayed columns")

    parttitle = Attribute("The title of the custom part")

    customparthead = Attribute("The custom part header line definitions")

    custompartdata = Attribute("The custom part data")

    custompartbarnames = Attribute("The custom part bar names")


class IContextStats(ICustomPart):
    """Interface for context related stats.
    """
