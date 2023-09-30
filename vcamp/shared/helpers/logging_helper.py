import logging


logger = logging.getLogger('django')

class UserIDXFilter(logging.Filter):
    def filter(self, record):
        try:
            from vcamp.log_middleware import thread_local
            record.user_idx = thread_local.user_idx
        except AttributeError:
            record.user_idx = None
        return True