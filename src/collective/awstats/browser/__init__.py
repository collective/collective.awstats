from Products.Five import BrowserView


class StatsTab(BrowserView):

    def __call__(self):
        try:
            field = self.context.getField('awstats_enabled')
        except AttributeError, e:
            return False
        return field.get(self.context)
