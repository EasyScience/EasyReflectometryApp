# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import Functions, Config


CONFIG = Config.Config(sys.argv[1], sys.argv[2])

def source():
    return os.path.basename(CONFIG.setup_zip_path)

def destination():
    return CONFIG.dist_dir

def createDestinationDir():
    Functions.createDir(CONFIG.dist_dir)

def unzipAppInstaller():
    Functions.unzip(source(), destination())

if __name__ == "__main__":
    createDestinationDir()
    unzipAppInstaller()
