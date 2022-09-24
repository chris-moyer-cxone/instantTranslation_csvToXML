'''
Author: Chris Moyer
Description: Takes a CSV and returns an XML file formatted appropriately for usage as a Custom Dictionary with CXone Expert.
'''

from functools import partial
import csv
from pathlib import Path
from pprint import pprint
from xml.dom import minidom
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from langDictionary import LangTerm, LangDict
import argparse
import os
import glob
import pandas as pd



# Configuration

outPath = Path('./Result/output.xml')
errorPath = Path('errors.csv')
dupePath = Path('./Result/duplicates.csv')
headerExist = True
langCheck = True

# End Configuration

# region args

parser = argparse.ArgumentParser(description="Takes an XLSX or UTF-8 encoded CSV and returns an XML file formatted appropriately for usage as a Custom Dictionary with CXone Expert.")

parser.add_argument('--source', type=Path, nargs='?', help='Path to an xlsx or csv file with translation language code, key, and value terms. Defaults to the most recently modified file in the local "Source" folder.')
parser.add_argument('--sheet', type=str, nargs='?', help='Only needed when providing .xlsx files. Name of the sheet where the source data is located.')
parser.add_argument('--allowed', type=Path, nargs='?', help='Path to a csv file containing the region description and the corresponding language code. Defaults to "allowedLanguageCodes.csv" in the local directory.')
parser.add_argument('--headerExists', default=False, action='store_true', help='Add this flag when a header row exists.')
parser.add_argument('--bypassLangCheck', default=False, action='store_true', help='Bypasses the language code check.')
parser.add_argument('--verbose', default=False, action='store_true', help='Prints debugging information.')

args = parser.parse_args()

# endregion 

# region Setup

# Supported Language Code Setup
# Allowed Language Codes: https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html
langSrc = args.allowed if args.allowed else Path('allowedLanguageCodes.csv')
langDict = {}
langCodes = []

langCodesDF = pd.read_csv(langSrc)
langCodes = list(langCodesDF.code)
languages = list(langCodesDF.language)

# Default Source File Setup
srcFiles = glob.glob('Source/*.csv')
if len(srcFiles) > 0:
    # Get the most recently modified file in the local Source folder
    inPath = Path( max( srcFiles, key=os.path.getmtime ) )
else:
    inPath = None

inPath = args.source if args.source else inPath
if args.verbose:
    print(f"Path to source file: {inPath}")

# endregion

# region General Helpers

class UnsupportedFileExtension(Exception): pass
class ExcelSheetNameRequired(Exception): pass

def ingestStructuredData(p:Path, sheet:str=None) -> list:
    '''Takes in a path, returns either a list of rows or None if something went wrong.'''
    extension = p.suffix

    if extension == '.xlsx': 
        if sheet == None: raise ExcelSheetNameRequired('When using .xlsx files, you must include the \
            --sheet argument and the name of the sheet where data lives.')
        return pd.read_excel( p, sheet ).values.tolist()
    elif extension == '.csv': return pd.read_csv( p ).values.tolist()
    else: 
        raise UnsupportedFileExtension('Only .xlsx or .csv files are supported.')

# endregion



# region Error Checking

options = [args.headerExists, args.bypassLangCheck, args.verbose]

class LanguageCodeError(Exception):
    pass

def errorChecker(rows, options):
    headerExist, checkLang, verbose = options

    onErrorMessage = f"See line errors.csv for a list of rows with invalid language codes.\nVisit https://success.mindtouch.com/Admin/Instant_Translation/Reference_for_Language_Codes for more information." 

    header = [['source row number', 'language code', 'findTerm', 'replaceTerm']]
    langMap = {}
    errorRows = []
    dupeRows = []

    for index, (lang, findTerm, replaceTerm) in enumerate(rows):
        if lang not in langMap: langMap[lang] = LangDict(lang)
        langMap[lang].terms.append( LangTerm( findTerm, replaceTerm, srcRow=index) )

        if checkLang and lang not in langCodes:
            # rows already has reduced the row count by 1 compared to source
            # For some reason, this means I need to increment by 1 more than below
            # to accommodate this shift.
            rowNum = index + 3 if headerExist else index + 2
            errorRows.append([rowNum, lang, findTerm, replaceTerm])
            continue
        
    if errorRows != []:
        header.extend(errorRows)
        with errorPath.open('w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(header)
        print(onErrorMessage)

    for mapKey in langMap:
        dictionary = langMap[mapKey]
        duplicates = dictionary.getDuplicates()
        if duplicates: print('Duplicates:')
        for term in duplicates:
            print(term)
            dupeRows.append([term.srcRowNum, dictionary.langCode, term.key, term.value])
    
    if dupeRows != []:
        dupeRows.sort(key=lambda e: e[0])
        with dupePath.open('w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(dupeRows)

    for langCode in langMap:
        langDictionary = langMap[langCode]
        for term in langDictionary.terms:
            if verbose:
                print(f"{langDictionary.langCode}: {term}")


# endregion

# region XML Helpers

def createEl(tag:str,parent:ET.Element, *_,  attrs:dict=None, text:str=None )-> ET.Element:
    if parent == None:
        el = ET.Element(tag)
    else:
        el = ET.SubElement(parent, tag)
    if attrs:
        for key in attrs:
            el.set(key, attrs[key])
    if text: el.text = text
    return el

createDictionaries = partial(createEl, 'dictionaries')
createDictionary = partial(createEl, 'dictionary')
createTerm = partial(createEl, 'term')
createKey = partial(createEl, 'key')
createValue = partial(createEl, 'value')

def xmlToString(data:ET.Element):
    # Removed xml_declaration=None from ET.tostring() to support Python 3.6
    return minidom.parseString(ET.tostring(data , encoding='utf-8', method='html')).toprettyxml(indent="   ")

def writeToFile(data:ET.Element, path:Path):
    outString = xmlToString(data)
    tmpString = ''
    with path.open('w', encoding='utf-8') as file:
        file.write(outString)
    with path.open('r', encoding='utf-8') as file:
        # remove the xml version line introduced by minidom.parseString
        tmpString = file.readline() 
        tmpString = file.read()
    with path.open('w', encoding='utf-8') as file:
        file.write(tmpString)

def getExistingDictionary(root: Element, langCode: str) -> Element:
    dictionaries = root.findall('dictionaries/dictionary')
    for d in dictionaries:
        lang = d.get('language')
        if lang == langCode: return d
    return None

# endregion 

# region Main

def csvToXml(rows):
    root = createEl('script', None, attrs={"type":'text/xml'}) 
    dictionaries = createDictionaries(root)

    for index, row in enumerate(rows):
        if row[0] not in langCodes:
            rowNum = index + 2 if headerExist else index + 1
            message = f"Language code provided not allowed. See line {rowNum} in source CSV file.\nVisit https://success.mindtouch.com/Admin/Instant_Translation/Reference_for_Language_Codes for more information." 
            raise LanguageCodeError(message)
        existingDict = getExistingDictionary(root, row[0])
        if existingDict:
            dictionary = existingDict
        else:
            dictionary = createDictionary(dictionaries, attrs={'language':row[0]})
        term = createTerm(dictionary)
        key = createKey(term, text=row[1])
        value = createValue(term, text=row[2])

    writeToFile(root, outPath)
    print(f"Success! Your file is at {outPath.as_posix()}")


# endregion

if __name__ == "__main__":
    rows = ingestStructuredData(inPath, args.sheet)

    if args.verbose: pprint(rows)
    errorChecker(rows, options)
    csvToXml(rows)