# SPDX-FileCopyrightText: 2022 EasyReflectometry contributors
# <support@easyreflectometry.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the EasyReflectometry project
# <https://github.com/easyScience/EasyReflectometryApp>

__author__ = ["github.com/AndrewSazonov", "github.com/arm61"]
__version__ = '0.0.1'

import os
import sys
import Functions
import Config

CONFIG = Config.Config()


def appExePath() -> str:
    """
    :return: Application executable path.
    """
    d = {
        'macos':
        os.path.join(CONFIG.installation_dir, CONFIG.app_full_name, 'Contents', 'MacOS',
                     CONFIG.app_name),
        'ubuntu':
        os.path.join(CONFIG.installation_dir, CONFIG.app_name, CONFIG.app_full_name),
        'windows':
        os.path.join(CONFIG.installation_dir, CONFIG.app_name, CONFIG.app_full_name)
    }
    return d[CONFIG.os]


def runApp():
    """
    Launch and run application.
    """
    Functions.printNeutralMessage(f'Installed application exe path: {appExePath()}')
    try:
        message = f'run {CONFIG.app_name}'
        if len(sys.argv) == 1:
            Functions.run(appExePath())
        else:
            print(appExePath())
            Functions.run(appExePath(), *sys.argv[1:])
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


if __name__ == "__main__":
    runApp()
