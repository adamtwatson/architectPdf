import logging
from logging import config


LOG_LEVEL = 'DEBUG'
LOG_NAME = 'Architect - PDF Generate'
LOG_FORMATTER = '[%(asctime)s] %(levelname)s [%(name)s:%(pathname)s:%(lineno)s] %(message)s'

# TODO get ENV from the environment
ENV = 'local'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMATTER,
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': LOG_FORMATTER,
            'datefmt': '%Y-%m-%dT%H:%M:%S%z'  # 2016-11-29T16:21:36+0000
        },
    },
    'filters': {
        # 'special': {
        #     '()': 'project.logging.SpecialFilter',
        #     'foo': 'bar',
        # }
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose' if ENV == 'local' else 'json'
        },
    },
    'loggers': {
        LOG_NAME: {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            # 'filters': ['special']
        }
    }
}


config.dictConfig(LOGGING)
logger = logging.getLogger(LOG_NAME)
