# SPDX-FileCopyrightText: 2022 EasyReflectometry contributors
# <support@easyreflectometry.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the EasyReflectometry project
# <https://github.com/easyScience/EasyReflectometryApp>

__author__ = ["github.com/AndrewSazonov", "github.com/arm61"]
__version__ = '0.0.1'

import sys
import Functions
import Config

CONFIG = Config.Config(sys.argv[1])


def source() -> str:
    """
    :return: Path to source executable that will be zipped.
    """
    return CONFIG.setup_exe_path


def destination() -> str:
    """
    :return: Path to destination for the zip.
    """
    return CONFIG.setup_zip_path


def zipAppInstaller():
    """
    Runs the zipping of the installer.
    """
    Functions.zip(source(), destination())


if __name__ == "__main__":
    zipAppInstaller()
