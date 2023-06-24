# Author: Vespertine112

from types import *
import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Clink, a config migration framework")
    parser.add_argument("-t", "--test", type=str, help="Test argument")
    parser.add_argument("-s", "--sync", action="store_true", help="Sync packages and configuration")
    parser.add_argument("-c", "--clank", action="store_true", help="Run the config migration")
    args = parser.parse_args()

    if (args.sync):
        sync()
        exit(1)

    



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
    check_push(subprocess.run(['git', 'push']))

    print("Sync Successful!")
        
def check_push(push_result:subprocess.CompletedProcess[bytes]):
    # Check the return code of the git push command
    if push_result.returncode != 0:
        print("Push failed. Performing git pull...")
        
        # Perform git pull
        pull_result = subprocess.run(['git', 'pull'])
        
        if pull_result.returncode != 0:
            print("Pull failed. Please resolve any conflicts manually.")
        else:
            print("Pull successful. Performing git push...")
            
            # Perform git push again after successful pull
            subprocess.run(['git', 'push'])
    else:
        print("Push successful.")  

if __name__ == "__main__":
    main()