# Base abstract class for the plugin template 
from abc import ABC, abstractmethod
from enum import Enum
import os

class Shell(Enum):
    zsh = 1
    pwrsh = 2
    bash = 3
    fish = 4

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

    @abstractmethod
    def get_config_files(self):
        """Config files should be a dict, with the name within dotfiles folder as key, and the location to extract to as value"""
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

    def run_plugins(self, dotfilePath):
        shell = os.environ.get('SHELL', '').lower()
        comspec = os.environ.get('COMSPEC', '').lower()

        live_shell = ""
        if 'bash' in shell:
            live_shell = Shell.bash
        elif 'zsh' in shell:
            live_shell = Shell.zsh
        elif 'fish' in shell:
            live_shell = Shell.fish
        elif 'powershell' in comspec:
            live_shell = Shell.pwrsh
        else:
            print("Failure to identify shell!")
            exit(-1)

        for plugin in self.plugins:
            plugin.download()
            plugin.install()
            plugin.configure(live_shell, dotfilePath)



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
