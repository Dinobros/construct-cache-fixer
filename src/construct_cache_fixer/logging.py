"""
A smarter logger module that provides some utilities
for a more convenient way to use the logging module.
"""

import logging
import os

from inspect import stack, getmodule


CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG


__level_to_name__ = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG'
}
__name_to_level__ = {
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG
}


class SmartLogger(logging.Logger):
    """
    A smarter logger implementation.

    It will automatically set the log level based on the 'LOG_LEVEL' environment variable.

    :param name: The name of the logger.
    :type name: str
    :param level: The log level of the logger.
    :type level: int | None

    :raises ValueError: If the 'LOG_LEVEL' environment variable is defined with an unknown value.
    """


    def __init__(self, name: str, level: int | None = None):
        if not level:
            level_name = os.environ.get('LOG_LEVEL', 'INFO')

            try:
                level = __name_to_level__[level_name]

            except KeyError as exc:
                raise ValueError(f"Unknown defined 'LOG_LEVEL' value: '{level_name}'") from exc

        super().__init__(name, level)

        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s (%(name)s on %(processName)s:%(threadName)s): %(message)s")

        handler.setFormatter(formatter)
        self.addHandler(handler)


logging.setLoggerClass(SmartLogger)


def getLogger(name: str | None = None) -> SmartLogger:
    """
    Returns a logger with the specified name.

    If the name is not specified, it will be the name
    of the module where the logger is being called.

    :param name: The name of the logger.
    :type name: str | None

    :return: The logger with the specified name.
    :rtype: SmartLogger
    """

    if not name:
        frame = stack()[1]
        module = getmodule(frame[0])
        if module:
            name = module.__name__

    return logging.getLogger(name)
