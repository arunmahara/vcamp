from .base import PAPERTRAIL_HOST, PAPERTRAIL_PORT

#loggers
LOGGING = {
    'version': 1,

    'disable_existing_loggers': False,

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'user_idx': {
            '()': 'vcamp.shared.helpers.logging_helper.UserIDXFilter'
        },
    },

    'formatters': {
            'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] [%(module)s] [%(lineno)s] [%(user_idx)s] [%(message)s]',
            },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'filters': ['require_debug_true'],
            'filters': ['user_idx'],
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            # 'filters': ['require_debug_true'],
            'filters': ['user_idx'],
            'filename': 'logs.log',
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        'papertrail': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',                                                    
            'formatter': 'verbose',
            'address': (PAPERTRAIL_HOST, PAPERTRAIL_PORT)                                                 
        },
    },

    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'papertrail'],
            'propagate': True,
        },

        #database query logger
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # }
    },
}