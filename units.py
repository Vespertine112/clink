# Base abstract class for the plugin template 

from abc import ABC, abstractmethod


class PluginScaffold(ABC):

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def install(self):
        pass
    
    @abstractmethod
    def configure(self):
        pass

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

    def list_plugins(self):
        for plugin in self.plugins:
            print(plugin)

    def run_plugins(self):
        for plugin in self.plugins:
            plugin.run()

class Logger:
    _instance = None
    log_file = "log.log"
    
    def __new__(cls, log_file):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.log_file = log_file
        return cls._instance
    
    def log(self, message):
        with open(self.log_file, 'a') as file:
            file.write(message + '\n')    
