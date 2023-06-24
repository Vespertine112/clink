from units import PluginScaffold

class PluginController:
    """The plugin controller maintains the list of all plugins and controls their execution"""
    _instance = None
    plugins:PluginScaffold

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.plugins = []
        return cls._instance

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def run_plugins(self):
        for plugin in self.plugins:
            plugin.run()