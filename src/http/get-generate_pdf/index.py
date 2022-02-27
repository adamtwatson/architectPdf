import base64
import codecs

from requests.exceptions import InvalidURL

from pdf_generator import PDFRenderer

# Arc Shared Code
from shared.settings import logger
from shared import db_repo
from shared.translations.i18n import i18n


def iterfile(target_file):
    # Adds byte mark order for UTF-8, https://en.wikipedia.org/wiki/Byte_order_mark
    yield codecs.BOM_UTF8
    # Syntax for Delegating to a Subgenerator, https://www.python.org/dev/peps/pep-0380/ for more info
    yield from target_file


@i18n  # This will harvest the translation data and add it to the event
def handler(event, context):
    """
    An endpoint that will create a translatable PDF file
    """
    # Make sure this is a valid request
    if not event['queryStringParameters']:
        logger.debug('Invalid request')
        raise InvalidURL('No Query String Found.')
    query_string_dict = event['queryStringParameters']

    # Get for the users data
    requested_user = query_string_dict.get('user', None)
    # Get the cat to see if the user owns
    validate_cat = query_string_dict.get('cat', None)
    assert requested_user is not None
    assert validate_cat is not None

    # Get the data for the request
    render_dict = db_repo.check_user_cat(user_id=requested_user, cat_id=validate_cat)

    # render the PDF file
    target_file = PDFRenderer(translations=event['translations'], data=render_dict).render()

    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": {"content-type": "application/pdf"},
        "body": base64.b64encode(target_file.read()).decode("utf-8")
    }
