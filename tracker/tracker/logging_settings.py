LOG_DIR="logs"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + "/tracker-app.log",
            'maxBytes': 1024*1024*50,     # 50 MB
            'backupCount': 10,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + "/access.log",
            'maxBytes': 1024*1024*500,         # 50 MB
            'backupCount': 5,
            'formatter': 'standard'
        },
    },
    'loggers': {
        'projects': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'accounts': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'home': {
            'handlers': ['logfile'],
            'level': "DEBUG"
        },
        'workflows': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'tasks': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}
