import json

import requests
import re
from shared import settings

import threading
import time

logger = settings.logger

libraries = [
    'boto3',
    'cffi',
    'chardet',
    'Django',
    'django-braces',
    'django-constance',
    'django-cors-headers',
    'django-environ',
    'django-filter',
    'django-model-utils',
    'django-picklefield',
    'djangorestframework',
    'docxtpl',
    'enum34',
    'idna',
    'ipaddress',
    'pathlib',
    'paramiko',
    'pika',
    'psycopg2',
    'pyasn1',
    'pycountry',
    'pycparser',
    'python-dateutil',
    'python-docx',
    'python-json-logger',
    'pytz',
    'requests',
    'sqlparse',
    'WeasyPrint',
    'Jinja2',
    'PyPDF2',
    'xlrd',
    'html5lib',
    'django-storages',
    'django-smuggler',
    'django-redis-cache',
    'rq',
    'rq-scheduler',
    'django-rq',
    'django-rq-scheduler',
    'django-sql-explorer'
]

base_url = 'https://pypi.org/project/'

regex = re.compile(r'(<strong>License:</strong>) (\w+)')

license_information = {}


def retrieve_license(library):
    logger.debug(f'Looking up license for: {library}')
    url = f'{base_url}{library}'
    logger.debug(f'Retrieving data from {url}')
    response = requests.get(url)
    # Find the license with the regex, only one needed
    groups = next(regex.finditer(response.text))
    # logger.debug(groups)
    library_license = 'No License!'
    if groups:
        # We only want the license information
        library_license = groups.groups()[1]
        logger.debug(library_license)
    # Update the dict
    license_information.update({library: library_license})


def handler(event, context):
    logger.debug(context)
    # Clean any dupes
    library_set_list = list(set(libraries))
    # Count what left
    key_count = len(library_set_list)
    # Keep looping until the set counts match
    while len(library_set_list) > 0:
        logger.debug(len(library_set_list))
        # loop to exhaustion, Each loop should remove an element and pass it to the thread function
        library = library_set_list.pop()
        x = threading.Thread(target=retrieve_license, args=(library,))
        x.start()
    while len(license_information.keys()) < key_count:
        sleep_time = 0.001
        logger.debug(f'Waiting for {sleep_time:.3f} seconds for licenses to finish')
        time.sleep(0.001)
    count_retrieved = len(license_information.keys())
    logger.debug(f'key_count: {key_count}')
    logger.debug(f'count_retrieved: {count_retrieved}')
    if key_count != count_retrieved:
        return {'body': license_information}
    else:
        logger.error('There was an error length of key_count is not equal')
        # Return what results we can
        return {'body': license_information}
