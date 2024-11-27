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

def checkAppExists():
    Functions.printNeutralMessage(f'Check if application exe file exists: {appExePath()}')
    message = f'find {appExePath()}'
    exists = pathlib.Path(appExePath()).is_file()
    if exists:
        Functions.printSuccessMessage(message)
    else:
        Functions.printFailMessage(message)
        sys.exit(1)

if __name__ == "__main__":
    checkAppExists()
