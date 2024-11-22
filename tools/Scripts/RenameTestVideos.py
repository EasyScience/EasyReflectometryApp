# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import Functions, Config


CONFIG = Config.Config(sys.argv[1])

def inputPath():
    return 'tutorial.mp4'

def outputPath():
    return CONFIG.video_tutorial_path

if __name__ == "__main__":
    Functions.copyFile(inputPath(), outputPath())
