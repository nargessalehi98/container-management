import logging
import traceback

logger = logging.getLogger(__name__)


def log_message(*, error, request):

    if request:
        message = '{error}'.format(
            error=error
        )
    else:
        message = '{error}'.format(error=error)
    return message


def log_error(message, *, request=None):
    _log_message = log_message(error=message, request=request)
    logger.error(_log_message)


def log_warning(message, *, request=None):
    _log_message = log_message(error=message, request=request)
    logger.warning(_log_message)

