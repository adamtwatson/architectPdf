# A dictionary containing language keys, and translations dictionary
import glob
import json
import os
from functools import wraps

from shared.settings import logger


def get_translations(locale):
    # Open the file
    with open(f"vendor/shared/translations/{locale}.json", 'r', encoding='utf8') as file:
        # Open the data as json and fill the translation dictionary
        translation_data = json.load(file)

    return translation_data


def available_locales():
    # Find all translation files
    language_list = glob.glob("vendor/shared/translations/*.json")
    # return a list of just the file name without extension as locale_keys
    return [os.path.basename(lang).split('.')[0] for lang in language_list]


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
        logger.debug(f"request: {request}")
        logger.debug(f"args: {args}")
        logger.debug(f"kwargs: {kwargs}")
        # Get all available translations
        locales = available_locales()
        # Default locale in case one doesnt exist on the request
        locale = 'en'
        locale_found = None

        # Check if we have a qs, and the qs has a locale
        if (params := request['queryStringParameters']) and ((param_locale := params.get('locale', None)) is not None):
            logger.debug(f'params: {params}')
            logger.debug(f'param_locale: {param_locale}')
            # Check for query strings for locale
            if param_locale in locales:
                # Set the locale
                locale = param_locale
                locale_found = True
        logger.debug(locale_found)
        # If we didn't find a local from the query string, use the user's system language
        if not locale_found and (accept_language := request['headers']['accept-language']):
            # 'en-US,en;q=0.9' will need to strip some extra info here
            accept_language = [v.split(';')[0] for v in accept_language.split(',')]
            # Find the first language that matches a translation key
            requested_lang = next(filter(lambda x: x in locales, accept_language))
            logger.debug(f'requested_lang: {requested_lang}')

            if requested_lang:
                # We found a requested translation override locale
                locale = requested_lang

        # Update context with translations data
        translations = get_translations(locale)
        request.update({'translations': translations})

        return func(request, *args, **kwargs)

    return wrapper
