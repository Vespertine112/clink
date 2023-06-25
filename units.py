# Base abstract class for the plugin template 
from abc import ABC, abstractmethod
from enum import Enum
import os
import subprocess
import sys
from typing import List

class Shell(Enum):
    zsh = 1
    pwrsh = 2
    bash = 3
    fish = 4

class OS(Enum):
    windows = 1
    linux = 2

class PluginScaffold(ABC):
    supported_platforms:List[OS] = []

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
    plugins:List[PluginScaffold] = []
    supported_platforms:OS = []
    dotfilesPath:str = ""

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
        shell = os.environ.get('SHELL', '').lower()
        comspec = os.environ.get('COMSPEC', '').lower()

        # Check shell & set enum
        live_shell:Shell = ""
        op_sys:OS = ""
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

        # Check OS and set enum
        if sys.platform.startswith('win'):
            op_sys = OS.windows
        elif sys.platform.startswith('linux'):
            op_sys = OS.linux
        else:
            print("Failure to identify operating system!")
            exit(-1)

        for plugin in self.plugins:
            if op_sys in plugin.supported_platforms:
                plugin.download()
                plugin.install()
                plugin.configure(live_shell, op_sys, self.dotfilesPath)
            else:
                print(f"Your operating system does not support {plugin}")
    
    def install_packages(self):
        # Read package names from pkglist.txt
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pkgcache', 'pkglist.txt'), 'r') as file:
            packages = file.read().splitlines()

        # Install packages with pacman
        pacman_command = ['pacman', '--noconfirm', '-Sy']
        pacman_command.extend(packages)
        subprocess.run(pacman_command, shell=True, check=True)

        # Read package names from pkglist_aur.txt
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pkgcache', 'pkglist_aur.txt'), 'r') as file:
            packages_aur = file.read().splitlines()

        # Install packages with yay
        yay_command = ['yay', '--noconfirm', '-Sy']
        yay_command.extend(packages_aur)
        subprocess.run(yay_command, shell=True, check=True)


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

def export(env_vars:dict):
    for k,v in env_vars.items():
        sh_code = f"""
        export {k}={v}
        """

        # Write the sh code to a temporary file
        sh_filename = 'export.sh'
        with open(sh_filename, 'w') as sh_file:
            sh_file.write(sh_code)

        # Execute the sh file
        subprocess.run(['sh', sh_filename], check=True)

        # Delete the sh file
        # subprocess.run(['rm', sh_filename])

        # Alternatively, for Windows, use the following to delete the sh file:
        # subprocess.run(['del', sh_filename], shell=True)
        
