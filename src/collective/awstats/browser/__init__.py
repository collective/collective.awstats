from Products.Five import BrowserView


class StatsTab(BrowserView):

    def __call__(self):
        try:
            field = self.context.getField('awstats_enabled')
            return field.get(self.context)
        except AttributeError, e:
            return False
