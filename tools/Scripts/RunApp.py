# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import pathlib
import Functions, Config


CONFIG = Config.Config()

def appExePath():
    d = {
        'macos': os.path.join(CONFIG.installation_dir, CONFIG.app_full_name, 'Contents', 'MacOS', CONFIG.app_name),
        'ubuntu': os.path.join(CONFIG.installation_dir, CONFIG.app_name, CONFIG.app_full_name),
        'windows': os.path.join(CONFIG.installation_dir, CONFIG.app_name, CONFIG.app_full_name)
    }
    return d[CONFIG.os]

def runApp():
    Functions.printNeutralMessage(f'Installed application exe path: {appExePath()}')
    try:
        message = f'run {CONFIG.app_name}'
        if len(sys.argv) == 1:
            Functions.run(appExePath())
        else:
            #if 'test' in sys.argv[1:]:
            #    Functions.createDir(CONFIG.screenshots_dir)
            Functions.run(appExePath(), *sys.argv[1:])
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


if __name__ == "__main__":
    runApp()
