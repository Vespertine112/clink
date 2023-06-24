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
    