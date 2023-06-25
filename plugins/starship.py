from units import PluginScaffold, Shell
import subprocess
import os

class starship(PluginScaffold):
    plugin_name = "starship"

    def __repr__(self):
        return self.plugin_name
    
    def get_config_files(self):
        config = {
            "starship.toml": "~/.config/"
        }
        return config

    def download(self):
        """Download also handles installation"""
        command = ["curl", "-sS", "https://starship.rs/install.sh"]
        subprocess.run(command, shell=False, check=True, text=True, capture_output=True)

    def install(self):
        pass
    
    def configure(self, shell:Shell, dotfilePath:str):
        
        if (shell == Shell.pwrsh):
            print(f"Configuring for powershell")
            command = [
            'powershell',
            '-Command',
            f'$ENV:STARSHIP_CONFIG = "{dotfilePath}\\starship.toml"'
            ]
            subprocess.run(command, shell=False, check=True)

        if (shell == Shell.zsh):
            command = [
            'export',
            f'STARSHIP_CONFIG=~{dotfilePath}/starship.toml'
            ]
            subprocess.run(command, shell=True, check=True)