# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import xml.etree.ElementTree as ET
import deepl
import Functions, Config


AUTH_KEY = 'Authentication Key for DeepL API from https://www.deepl.com/account/summary'
QT_BIN_DIR = '/Users/as/Qt/6.5.0/macos/bin'
CONFIG = Config.Config()
TRANSLATOR = deepl.Translator(AUTH_KEY)

def tsFilesDirPath():
    ts_files_dir = CONFIG['ci']['app']['translations']['dir']
    return os.path.join(CONFIG.package_name, ts_files_dir)

def fromLanguage():
    return 'en'

def toLanguage(fpath):
    fname, _ = os.path.splitext(os.path.basename(fpath))
    return fname[-2:]

def tsFilePaths():
    languages = CONFIG['ci']['app']['translations']['languages']
    dir = tsFilesDirPath()
    fpaths = []
    for language in languages:
        code = language['code']
        fname = f'language_{code}.ts'
        fpath = os.path.join(dir, fname)
        if code != 'en':
            fpaths.append(fpath)
    return fpaths

def translateTsFiles():
    try:
        message = 'translate .ts files'
        for fpath in tsFilePaths():
            translateFile(fpath)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def translateFile(fpath):
    with open(fpath, 'r') as file :
        xml_string = file.read()
    translated_xml_string = translateXmlString(xml_string, fromLanguage(), toLanguage(fpath))
    with open(fpath, 'w') as file:
        file.write(translated_xml_string)

def translateXmlString(xml_string, from_language, to_language):
    Functions.printNeutralMessage(f'Translating to {to_language}')
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot()
    for context in root.iter('context'):
        for message in context.iter('message'):
            source = message.find('source')
            translation = message.find('translation')
            if translation.text == None:
                translation.text = translateText(source.text, from_language, to_language)
            if translation.attrib.get('type') == 'unfinished':
                del translation.attrib['type']
    return ET.tostring(root, encoding='utf8').decode('utf8')

def translateText(in_text, from_language, to_language):
    result = TRANSLATOR.translate_text(in_text, source_lang=from_language, target_lang=to_language)
    out_text = result.text
    Functions.printNeutralMessage(f'[{from_language}] {in_text} -> [{to_language}] {out_text}')
    return out_text

def updateTsFiles():
    try:
        message = 'update .ts files'
        qt_lupdate_path = f'{QT_BIN_DIR}/lupdate'
        ts_files = tsFilePaths()
        Functions.run(
            qt_lupdate_path,
            '.',
            '-extensions', 'qml',
            '-ts', *ts_files
        )
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def releaseTsFiles():
    try:
        message = 'release .ts files'
        qt_lrelease_path = f'{QT_BIN_DIR}/lrelease'
        ts_files = tsFilePaths()
        Functions.run(
            qt_lrelease_path,
            *ts_files
        )
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

if __name__ == "__main__":
    # also need method to create ts files, if those are not created yet

    updateTsFiles()
    translateTsFiles()
    releaseTsFiles()
