# Usage 

This guide assumes basic knowledge of command prompt or terminal and knowledge of how to execute Python scripts on your computer.

## Requirements
- Python 3.6+
- Pandas Python Library is downloaded
> 🎈 If you have Pip installed, you can run `pip install pandas`


## General Usage
- Place the customer's customDictionarySource.csv file into the Source folder
- Execute "python main.py" if no header exists in the CSV file. "python main.py -headerExists" if one does.
>  🎈 Since the provided sample CSV file contains a header row, the default example below includes the -headerExists flag

- The resulting "output.xml" file will appear in the Result folder
    - output.xml will be overwritten on next execution. Be sure to rename output.xml if you need to keep it.

- The contents of the XML file need to be copied and pasted into the appropriate template in the customer's site.
### Notes
- Duplicates are automatically removed. Duplicate terms are output as a CSV file in the Result file for reference.

## Examples

Default Run Command
```
python main.py -headerExists
```

Specific Source File
```
python main.py -source .\Source\customDictionarySource.csv
```

When providing a path on Windows, use the \ character to separate Path elements. 
On Mac or Linux, use the / character.

Use Most Recently Modified CSV File in Source, and Header Row Exists
```
python main.py -headerExists
```

Example Troubleshooting Command
```
python main.py -source .\Source\customDictionarySource.csv -bypassLangCheck -verbose
```

## Flags

| flag  |  description |
|-------|-------------|
| --source  |  Path to a csv file with translation language code, key, and value terms. Defaults to the most recently modified file in the local "Source" folder. |
| --sheet | **Only required when supplying a .xlsx file.** Text string representing the name of the sheet where the source data is stored. |
| --allowed  |  Path to a csv file containing the region description and the corresponding language code. Defaults to "allowedLanguageCodes.csv" in the local directory. |
| --headerExists  |  Add this flag when a header row exists. |
| --bypassLangCheck  |  Bypasses the language code check. |
| --verbose  |  Prints debugging information. |

# Supported Language Codes

This list is determined by AWS. [Visit here](https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html) for the most up to date list of supported languages.

| Language  |  Language code |
|------------|---------------|
| Afrikaans  |  af |
| Albanian  |  sq |
| Amharic  |  am |
| Arabic  |  ar |
| Armenian  |  hy |
| Azerbaijani  |  az |
| Bengali  |  bn |
| Bosnian  |  bs |
| Bulgarian  |  bg |
| Catalan  |  ca |
| Chinese (Simplified)  |  zh |
| Chinese (Traditional)  |  zh-TW |
| Croatian  |  hr |
| Czech  |  cs |
| Danish  |  da |
| Dari  |  fa-AF |
| Dutch  |  nl |
| English  |  en |
| Estonian  |  et |
| Farsi (Persian)  |  fa |
| Filipino, Tagalog  |  tl |
| Finnish  |  fi |
| French  |  fr |
| French (Canada)  |  fr-CA |
| Georgian  |  ka |
| German  |  de |
| Greek  |  el |
| Gujarati  |  gu |
| Haitian Creole  |  ht |
| Hausa  |  ha |
| Hebrew  |  he |
| Hindi  |  hi |
| Hungarian  |  hu |
| Icelandic  |  is |
| Indonesian  |  id |
| Irish  |  ga |
| Italian  |  it |
| Japanese  |  ja |
| Kannada  |  kn |
| Kazakh  |  kk |
| Korean  |  ko |
| Latvian  |  lv |
| Lithuanian  |  lt |
| Macedonian  |  mk |
| Malay  |  ms |
| Malayalam  |  ml |
| Maltese  |  mt |
| Marathi  |  mr |
| Mongolian  |  mn |
| Norwegian (Bokmål)  |  no |
| Pashto  |  ps |
| Polish  |  pl |
| Portuguese (Brazil)  |  pt |
| Portuguese (Portugal)  |  pt-PT |
| Punjabi  |  pa |
| Romanian  |  ro |
| Russian  |  ru |
| Serbian  |  sr |
| Sinhala  |  si |
| Slovak  |  sk |
| Slovenian  |  sl |
| Somali  |  so |
| Spanish  |  es |
| Spanish (Mexico)  |  es-MX |
| Swahili  |  sw |
| Swedish  |  sv |
| Tamil  |  ta |
| Telugu  |  te |
| Thai  |  th |
| Turkish  |  tr |
| Ukrainian  |  uk |
| Urdu  |  ur |
| Uzbek  |  uz |
| Vietnamese  |  vi |
| Welsh  |  cy |