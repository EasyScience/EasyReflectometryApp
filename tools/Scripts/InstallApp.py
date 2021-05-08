__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import Functions, Config


CONFIG = Config.Config()

def setupExePath():
    d = {
        'macos': os.path.join(CONFIG.setup_full_name, 'Contents', 'MacOS', CONFIG.setup_name),
        'ubuntu': CONFIG.setup_full_name,
        'windows': CONFIG.setup_full_name
    }
    return os.path.join(CONFIG.dist_dir, d[CONFIG.os])

def runInstallerSilently():
    try:
        message = f'install {CONFIG.app_name}'
        silent_script = CONFIG['ci']['scripts']['silent_install']
        silent_script_path = os.path.join(CONFIG.scripts_dir, silent_script)
        Functions.installSilently(
            installer=setupExePath(),
            silent_script=silent_script_path
        )
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

if __name__ == "__main__":
    runInstallerSilently()
