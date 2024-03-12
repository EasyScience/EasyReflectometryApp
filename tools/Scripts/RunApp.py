__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import Functions, Config
import time

CONFIG = Config.Config()
DELAYED_QUIT = 30

def appExePath() -> str:
    """
    :return: Application executable.
    """
    d = {
        'macos': os.path.join(CONFIG.installation_dir, CONFIG.app_full_name, 'Contents', 'MacOS', CONFIG.app_name),
        'ubuntu': os.path.join(CONFIG.installation_dir, CONFIG.app_name, CONFIG.app_full_name),
        'windows': os.path.join(CONFIG.installation_dir, CONFIG.app_name, CONFIG.app_full_name)
    }
    return d[CONFIG.os]

def runApp():
    """
    Runs the application. 
    """
    Functions.printNeutralMessage(f'Installed application exe path: {appExePath()}')
    try:
        message = f'run {CONFIG.app_name}'
        if len(sys.argv) == 1:
            Functions.run(appExePath())
        elif sys.argv[1] == '--testmode':
            time_start = time.time()
            Functions.run(appExePath(), '--testmode')
            time_end = time.time()
            if time_end - time_start < DELAYED_QUIT:
                # Delay is set in UserTutorialsController.qml
                Functions.printFailMessage(f"Application ran for less the {DELAYED_QUIT} sec. Probably import error.")
                sys.exit(1)
        else:
            #if 'test' in sys.argv[1:]:
            #    Functions.createDir(CONFIG.screenshots_dir)
            Functions.run(appExePath(), *sys.argv[1:])
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)


if __name__ == "__main__":
    runApp()
