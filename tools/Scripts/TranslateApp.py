__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import xml.etree.ElementTree as ET
#import googletrans
import google_trans_new
import PySide2
import Functions, Config


CONFIG = Config.Config()
#TRANSLATOR = googletrans.Translator()
TRANSLATOR = google_trans_new.google_translator()

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
    #translation = TRANSLATOR.translate(in_text, src=from_language, dest=to_language)
    #out_text = translation.text
    out_text = TRANSLATOR.translate(in_text, lang_src=from_language, lang_tgt=to_language)
    print(f'[{from_language}] {in_text} -> [{to_language}] {out_text}')
    if isinstance(out_text, list):
        out_text = out_text[0]
    if in_text[0].isupper():
        out_text = out_text.capitalize()
    return out_text

def updateTsFiles():
    try:
        message = 'update .ts files'
        qt_lupdate_path = '/Users/andrewsazonov/Qt5.14.1/5.14.1/clang_64/bin/lupdate'
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
        qt_lrelease_path = '/Users/andrewsazonov/Qt5.14.1/5.14.1/clang_64/bin/lrelease'
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
    updateTsFiles()
    translateTsFiles()
    releaseTsFiles()
