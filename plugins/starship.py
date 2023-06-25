from units import PluginScaffold, Shell, OS
import subprocess
import os

class starship(PluginScaffold):
    plugin_name = "starship"
    supported_platforms:OS = [OS.linux, OS.windows]

    def __repr__(self):
        return self.plugin_name
    
    def get_config_files(self):
        config = {
            "starship.toml": "~/.config/"
        }
        return config

    def download(self):
        """Download also handles installation"""
        command = [
            'curl',
            '-sS',
            'https://starship.rs/install.sh'
        ]
        curl_process = subprocess.Popen(command, stdout=subprocess.PIPE)
        subprocess.run(['sh'], stdin=curl_process.stdout, check=True)


    def install(self):
        pass
    
    def configure(self, shell:Shell, op_sys:OS, dotfilePath:str):
        
        if (shell == Shell.pwrsh and op_sys == OS.windows):
            print(f"Configuring for powershell")
            command = [
            'powershell',
            '-Command',
            f'$ENV:STARSHIP_CONFIG = "{dotfilePath}\\starship.toml"'
            ]
            subprocess.run(command, shell=False, check=True)

        if (shell in [Shell.zsh, Shell.bash, Shell.fish] and op_sys == OS.linux):
            command = [
            'export',
            f'STARSHIP_CONFIG=~{dotfilePath}/starship.toml'
            ]
            subprocess.run(command, shell=True, check=True)