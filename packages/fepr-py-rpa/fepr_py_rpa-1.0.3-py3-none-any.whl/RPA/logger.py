from logging import config, getLogger, DEBUG

config.dictConfig({
    'version': 1,
    'formatters': {
        'defaltFormatter': {
            'format': '[%(asctime)s] [%(levelname)s] [%(funcName)s] : %(message)s'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'formatter': 'defaltFormatter',
            'level': DEBUG
        }
    },
    'root': {
        'handlers': ['consoleHandler'],
        'level': DEBUG
    },
    'loggers': {
        'defalt': {
            'handlers': ['consoleHandler'],
            'level': DEBUG,
            'propagate': 0
        }
    }
})

logger = getLogger('defalt')

