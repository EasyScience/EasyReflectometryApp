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


def source():
    return CONFIG.setup_exe_path


def destination():
    return CONFIG.setup_zip_path


def zipAppInstaller():
    Functions.zip(source(), destination())


if __name__ == "__main__":
    zipAppInstaller()
