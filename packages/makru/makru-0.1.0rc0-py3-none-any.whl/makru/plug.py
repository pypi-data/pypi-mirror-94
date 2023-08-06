from pluginbase import PluginBase


class PlugBox(object):
    def __init__(self):
        self.pbase = PluginBase(
            package="makru.plugins",
        )
        self.searchpaths = []
        self._source = None

    def source(self):
        if self._source:
            return self._source
        self._source = self.pbase.make_plugin_source(
            searchpath=self.searchpaths,
            persist=True,
        )
        return self._source

    def plugin_names(self):
        return self.source().list_plugins()

    def exists(self, name: str):
        return name in self.plugin_names()

    def load(self, name: str):
        return self.source().load_plugin(name)

    def runhook(self, name: str, *args, **kvargs):
        for n in self.plugin_names():
            p = self.load(n)
            if hasattr(p, name):
                getattr(p, name)(*args, **kvargs)
