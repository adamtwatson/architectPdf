import base64
import codecs

import os
from io import BytesIO

from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

from shared import settings

from shared.translations import i18n

logger = settings.logger


def environment():
    """
    Set up the jinja2 with File Loader.
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'templates')

    j2_env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
    )

    return j2_env


def iterfile(target_file):
    # Adds byte mark order for UTF-8, https://en.wikipedia.org/wiki/Byte_order_mark
    yield codecs.BOM_UTF8
    # Syntax for Delegating to a Subgenerator, https://www.python.org/dev/peps/pep-0380/ for more info
    yield from target_file


def handler(event, context):
    """
    An endpoint that will create a translatable PDF file
    """
    logger.debug(event)
    logger.debug(context)
    # Get the locale from the headers
    locale = event['queryStringParameters'].get('locale', None)
    translations = i18n.get_translations()
    # Make sure the requested local actually exists in language keys, otherwise default to english
    if locale not in translations.keys():
        logger.debug(f'Requested locale: {locale}, not available, defaulting to en')
        locale = 'en'

    # Update context with translations data
    context.update(translations[locale])
    # Assert the system generated translations
    assert context is not None
    # TODO MAKE SURE NO KEYS IN CONTEXT MATCH THE TRANSLATIONS IN THE LANGUAGE JSON FILES
    data_dict = {
        'data_point_1': 'Testing 123',
        'data_point_2': 'Testing 456',
        'data_point_3': 'Testing 789',
        # 'title': "We don't want to overwrite this key because it is a translation"
    }

    # Assert we are not trying to update a translation
    key_collision = set(data_dict.keys()).intersection(context.keys())
    assert len(key_collision) == 0

    context.update(data_dict)
    logger.debug(f'context: {context}')

    # Grab the template
    template = environment().get_template('pdf_template.html')
    # Pass the context data to the template, this includes translation context keys
    html = template.render(context)
    # Create a bytes io object to store the pdf we are creating
    target_file = BytesIO()
    # Create the PDF, using the ByteIO object as the target file
    HTML(string=html).write_pdf(target=target_file)
    # Set the BytesIO file buffer's current position to 0, this lets the file be iterated from the start
    target_file.seek(0)
    return {
      "isBase64Encoded": True,
      "statusCode": 200,
      "headers": {"content-type": "application/pdf"},
      "body": base64.b64encode(target_file.read()).decode("utf-8")
    }
