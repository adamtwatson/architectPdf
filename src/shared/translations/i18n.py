# A dictionary containing language keys, and translations dictionary
import glob
import json
import os


from shared import settings
logger = settings.logger


def get_translations():
    translation_data = {}
    # Find all translation files
    language_list = glob.glob("vendor/shared/translations/*.json")
    logger.debug(language_list)

    # Loop the language files and fill the dictionary with key and values
    for lang in language_list:
        filename = os.path.basename(lang)
        # Use the file name as the key,
        lang_code, ext = os.path.splitext(filename)
        # Open the file
        with open(lang, 'r', encoding='utf8') as file:
            # Open the data as json and fill the translation dictionary
            translation_data[lang_code] = json.load(file)

    return translation_data
