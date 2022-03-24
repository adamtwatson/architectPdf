import json
from pathlib import Path
from unittest import TestCase

from shared.translations import i18n


current_path = Path(__file__).resolve().parent


class Test(TestCase):

    def setUp(self) -> None:
        with open(f"{current_path}/en.json", 'r', encoding='utf8') as file:
            # Open the data as json and fill the translation dictionary
            self.expected_translations_default = json.load(file)

        self.expected_translations_en = self.expected_translations_default

        with open(f"{current_path}/de.json", 'r', encoding='utf8') as file:
            self.expected_translations_de = json.load(file)

    def tearDown(self) -> None:
        pass

    def test_get_translation_for_locale(self):
        en_translations = i18n.get_translation_for_locale('en')
        self.assertDictEqual(self.expected_translations_en, en_translations)
        de_translations = i18n.get_translation_for_locale('de')
        self.assertDictEqual(self.expected_translations_de, de_translations)
        self.assertRaises(i18n.LocaleNotFound, i18n.get_translation_for_locale, 'doesnt-exist')

    def test_available_locales(self):
        locales = i18n.available_locales()
        self.assertIn('en', locales)
        self.assertIn('de', locales)

    def test_harvest_locale(self):
        # Test no locales
        request = dict()
        locale = i18n.harvest_locale(request)
        self.assertEqual(locale, 'en')

        # Test en locales
        request = dict()
        request['headers'] = {'accept-language': 'en'}
        locale = i18n.harvest_locale(request)
        self.assertEqual(locale, 'en')
        request = dict()
        request['queryStringParameters'] = {'locale': 'en'}
        locale = i18n.harvest_locale(request)
        self.assertEqual(locale, 'en')

        # Test de locales
        request = dict()
        request['headers'] = {'accept-language': 'de'}
        locale = i18n.harvest_locale(request)
        self.assertEqual(locale, 'de')
        request = dict()
        request['queryStringParameters'] = {'locale': 'de'}
        locale = i18n.harvest_locale(request)
        self.assertEqual(locale, 'de')

        # Test non-existent locales default to en
        request = dict()
        request['headers'] = {'accept-language': 'doesnt-exist'}
        locale = i18n.harvest_locale(request)
        self.assertEqual(locale, 'en')

        request = dict()
        request['queryStringParameters'] = {'locale': 'doesnt-exist'}
        locale = i18n.harvest_locale(request)
        self.assertEqual(locale, 'en')

    def test_i18n(self):
        request = dict()
        response = i18n.i18n(lambda x: x)(request)
        self.assertDictEqual(self.expected_translations_default, response['translations'])
        request['queryStringParameters'] = {'locale': 'en'}
        response = i18n.i18n(lambda x: x)(request)
        self.assertDictEqual(self.expected_translations_en, response['translations'])

        request['queryStringParameters'] = {'locale': 'de'}
        response = i18n.i18n(lambda x: x)(request)
        self.assertDictEqual(self.expected_translations_de, response['translations'])

        request = dict()
        request['headers'] = {'accept-language': 'en'}
        response = i18n.i18n(lambda x: x)(request)
        self.assertDictEqual(self.expected_translations_en, response['translations'])

        request['headers'] = {'accept-language': 'de'}
        response = i18n.i18n(lambda x: x)(request)
        self.assertDictEqual(self.expected_translations_de, response['translations'])
