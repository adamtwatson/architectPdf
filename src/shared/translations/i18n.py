# A dictionary containing language keys, and translations dictionary
import glob
import json
import os
from functools import wraps
from pathlib import Path

from shared.settings import logger

current_path = Path(__file__).resolve().parent


class LocaleNotFound(Exception):
    pass


def available_locales():
    # Find all translation files
    language_list = glob.glob(f"{current_path}/*.json")
    # return a tuple of just the file name without extension as locale_keys
    return tuple([os.path.basename(lang).split('.')[0] for lang in language_list])


def get_translation_for_locale(locale):
    """Returns translations for the request local"""
    if locale not in available_locales():
        raise LocaleNotFound(f'The requested locale: {locale}, was not found.')
    # Open the file
    with open(f"{current_path}/{locale}.json", 'r', encoding='utf8') as file:
        # Open the data as json and fill the translation dictionary
        translation_data = json.load(file)

    return translation_data


def harvest_locale(request):
    # Get all available translations
    locales = available_locales()
    # Default locale in case one does not exist on the request
    locale = 'en'
    locale_found = None
    # Check if we have a qs, and the qs has a locale
    if 'queryStringParameters' in request.keys():
        if (params := request['queryStringParameters']) and ((param_locale := params.get('locale', None)) is not None):
            # Check for query strings for locale
            if param_locale in locales:
                # Set the locale
                locale = param_locale
                locale_found = True

    if 'headers' in request.keys():
        # If we didn't find a local from the query string, use the user's system language
        if not locale_found and (accept_language := request['headers']['accept-language']):
            # 'en-US,en;q=0.9' will need to strip some extra info here
            accept_language = (v.split(';')[0] for v in accept_language.split(','))
            for lang in accept_language:
                # Find the first language that matches a translation key and break
                if lang in locales:
                    locale = lang
                    break

    return locale


def i18n(func):
    """
    Decorator to make a view check for requested translations and add it to the request. Default 'en'  Usage::

        @i18n
        def my_view(request):
            # I can assume now that the request will have a request.translations associated with it
            # ...
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Get the locale from the request
        locale = harvest_locale(request)

        # Update context with translations data
        translations = get_translation_for_locale(locale)
        request['translations'] = translations

        return func(request, *args, **kwargs)

    return wrapper
