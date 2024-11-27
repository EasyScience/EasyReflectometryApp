# SPDX-FileCopyrightText: 2023 EasyReflectometry contributors <support@easyreflectometry.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the EasyReflectometry project <https://github.com/easyScience/EasyReflectometryApp>

__author__ = 'github.com/AndrewSazonov'
__version__ = '0.0.1'

import os
import re
import sys

import Config
from gtts import gTTS

CONFIG = Config.Config()


def fileWithPhrases():
    return os.path.join(CONFIG.package_name, 'Gui', 'Pages', 'Home', 'MainContent.qml')
    # return os.path.join(CONFIG.package_name, 'Gui', 'Components', 'UserGuides.qml')


def phrasesList():
    pattern = 'say\(["\'](.+)["\']\)'
    # pattern = "qsTr\([\"\'](.+)[\"\']\)"
    with open(fileWithPhrases(), 'r') as f:
        lines = f.read()
        phrases = re.findall(pattern, lines)
    phrases = [p.replace('\\n', ' ') for p in phrases]
    return phrases


def audioDirPath():
    voices_dir = CONFIG['ci']['app']['audio']['dir']
    return os.path.join(CONFIG.package_name, voices_dir)


def audioFilePath(name):
    p = os.path.join(audioDirPath(), f'{name}.mp3')
    p = p.replace(' ', '_')
    return p


def createAudioFiles():
    for p in phrasesList():
        print(p)
        tts = gTTS(text=p, lang='en-au')
        tts.save(audioFilePath(p))


if __name__ == '__main__':
    createAudioFiles()
