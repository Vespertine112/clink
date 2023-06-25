# Author: Vespertine112

from units import *
import glob
import importlib
import argparse
import subprocess
import os

log_file = 'log.txt'
logger = Logger(log_file)


def main():
    parser = argparse.ArgumentParser(description="Clink, a config migration framework")
    parser.add_argument("-s", "--sync", action="store_true", help="Sync packages and configuration")
    parser.add_argument("-c", "--clank", action="store_true", help="Run the config migration")
    parser.add_argument("-l", "--list", action="store_true", help="List the packages which will be manually configured on clank")
    parser.add_argument("-d", "--dotfiles", type=str, help="Path for dotfiles. Needs to be a relative path from home dir!!!")
    args = parser.parse_args()

    if (args.list):
        list()

    if (args.sync):
        sync()
        exit(1)
    
    if (args.clank and args.dotfiles):
        clank(args.dotfiles)
        exit(1)

def list():
    PluginController().list_plugins()

def clank(dotfilesPath):
    PluginController().run_plugins(dotfilesPath)
    pass

def sync():
    """Grab or update a list of packages from pacman and Aur, then store them in the packages folder."""

    # Create the full path to the subdirectory
    subdirectory_path = os.path.join(os.getcwd(), "pkgcache")

    pkgTargets = {
        "pkglist.txt": ["pacman", "-Qqen"], 
        "pkglist_aur.txt": ["pacman","-Qqem"]
    }

    for target, commands in pkgTargets.items():
        file_path = os.path.join(subdirectory_path, target)

        if not os.path.exists(subdirectory_path):
            os.makedirs(subdirectory_path)

        with open(file_path, 'w') as targetFile:
            subprocess.run(commands, stdout=targetFile)

    subprocess.run(["git", "add", "pkgcache"])
    subprocess.run(['git', 'commit', '-m', "Sync package cache"])
    check_push(subprocess.run(['git', 'push'], capture_output=True, text=True))

    print("Sync Successful!")
        
def check_push(push_result:subprocess.CompletedProcess[bytes]):
    '''Check and handle a git push'''
    if push_result.returncode != 0:
        print("Push failed. Performing git pull...")        
        logger.log(push_result.stdout)
        pull_result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        if pull_result.returncode != 0:
            logger.log(pull_result.stdout)
            print("Pull failed. Please resolve any conflicts manually.")
        else:
            print("Pull successful. Performing git push...")
            subprocess.run(['git', 'push'])
    else:
        print("Push successful.")  

def load_plugin_modules():
    '''Loads all plugins modules and stores them on the controller'''
    module_files = glob.glob('plugins/*.py')
    for module_file in module_files:
        module_name = os.path.splitext(module_file)[0].replace('/', '.')  # Construct the module name
        module = importlib.import_module(module_name)
        
        # Get the class name (assuming the class name is the same as the module name)
        class_name = os.path.basename(module_file)[:-3]
        
        # Retrieve the class from the module
        class_ = getattr(module, class_name)
        
        # Instantiate the class
        PluginController().add_plugin(class_())

if __name__ == "__main__":
    load_plugin_modules()
    main()

