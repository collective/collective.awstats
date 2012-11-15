from zope.interface import implementer 
from interfaces import IAwstatsProvider


@implementer(IAwstatsProvider)
class AwstatsProvider(object):
    """Implementation details see interfaces.IAwstatsProvider.
    """

    def __init__(self, context):
        self.context = context

    @property
    def statsavailable(self):
        smt = self._getSmt()
        if not smt:
            return False
        return True

    @property
    def alloweddomains(self):
        smt = self._getSmt()
        if not smt:
            return []
        return smt.getAllowedDomains()

    def getAvailableYears(self, domain):
        smt = self._getSmt()
        if not smt:
            return []
        return smt.getAvailableYears(domain)

    def getStatistics(self, domain):
        smt = self._getSmt()
        return smt.getStatistics(domain)

    def reload(self, domain):
        smt = self._getSmt()
        smt.purge(domain)

    def _getSmt(self):
        try:
            return self.context.blueawstats_management_tool
        except:
            return None
