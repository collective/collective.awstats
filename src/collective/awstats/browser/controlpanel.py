from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from yafowil.plone.form import YAMLBaseForm
from ..interfaces import IAwstatsProvider
from .. import _


class AwstatsControlPanel(YAMLBaseForm):
    action_resource = 'awstats_controlpanel'
    form_template = 'collective.awstats.browser:controlpanel.yaml'
    message_factory = _

    @property
    def registry(self):
        return getUtility(IRegistry)

    @property
    def basedir_value(self):
        return self.registry['collective.awstats.basedir']

    @property
    def prefix_value(self):
        return self.registry['collective.awstats.prefix']

    @property
    def postfix_value(self):
        return self.registry['collective.awstats.postfix']

    @property
    def domains_value(self):
        return self.registry['collective.awstats.domains']

    @property
    def domains_vocab(self):
        domains = IAwstatsProvider(self.context).listAvailableDomains()
        return [domain for domain in domains if domain]

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('awstats.%s' % name).extracted
        reg = self.registry
        reg['collective.awstats.basedir'] = fetch('basedir').decode('utf-8')
        reg['collective.awstats.prefix'] = fetch('prefix').decode('utf-8')
        reg['collective.awstats.postfix'] = fetch('postfix').decode('utf-8')
        domains = [domain.decode('utf-8') for domain in fetch('domains')]
        reg['collective.awstats.domains'] = tuple(domains)

    def next(self, request):
        return
